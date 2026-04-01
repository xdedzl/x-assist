import sys
import os
import time
import threading
import ctypes


def enable_vt_mode():
    """启用 Windows 控制台的 VT100 (ANSI) 序列支持"""
    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(handle, ctypes.byref(mode))
    kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)


def main():
    # 启用 VT 模式，让 cmd 窗口能正确渲染 ANSI 转义序列
    try:
        enable_vt_mode()
    except Exception:
        pass

    # 参数 1: 模型名称 (必填)
    # 参数 2: 目标文件夹 (选填)
    model_name = sys.argv[1] if len(sys.argv) > 1 else "gpt-4.1"
    target_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    target_dir = target_dir.strip('"').rstrip('\\/') 
    target_dir = os.path.abspath(target_dir)

    print(f"--- Launching Copilot ({model_name}) ---")
    print(f"--- Folder: {target_dir} ---")
    print(f"--- Loading... ---")
    sys.stdout.flush()

    try:
        from winpty import PtyProcess
    except ImportError:
        print("ERROR: pywinpty not installed. Run: pip install pywinpty")
        return

    # 用 ConPTY 伪终端启动 copilot，让它以为自己连在真终端上
    try:
        proc = PtyProcess.spawn("copilot", cwd=target_dir)
    except Exception as e:
        print(f"ERROR: Failed to spawn copilot: {e}")
        return

    # 读取 pty 输出并实时转发到 stdout
    def read_output():
        try:
            while proc.isalive():
                try:
                    data = proc.read(4096)
                    if data:
                        sys.stdout.write(data)
                        sys.stdout.flush()
                except EOFError:
                    break
                except Exception as e:
                    print(f"\n[xassist] Read error: {e}", file=sys.stderr)
                    break
        except Exception:
            pass

    t_out = threading.Thread(target=read_output, daemon=True)
    t_out.start()

    # 等 copilot 加载
    time.sleep(6)

    # 发送初始命令
    try:
        proc.write("/allow-all\r\n")
        time.sleep(2)
        proc.write(f"/model {model_name}\r\n")
    except Exception as e:
        print(f"[xassist] Failed to send commands: {e}", file=sys.stderr)

    # 转发用户 stdin 到 copilot
    def forward_stdin():
        try:
            while proc.isalive():
                line = sys.stdin.readline()
                if not line:
                    break
                proc.write(line)
        except Exception:
            pass

    t_in = threading.Thread(target=forward_stdin, daemon=True)
    t_in.start()

    # 等待进程结束
    while proc.isalive():
        time.sleep(0.5)

    # 读取残留输出
    try:
        remaining = proc.read(4096)
        if remaining:
            sys.stdout.write(remaining)
            sys.stdout.flush()
    except Exception:
        pass

    print(f"\n--- Copilot exited with code {proc.exitstatus} ---")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")
