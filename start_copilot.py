import subprocess
import time
import ctypes
import sys
import os

# Windows API constants
SW_RESTORE = 9

def get_terminal_hwnds():
    """获取所有可能与 Terminal 相关的窗口句柄"""
    res = set()
    def callback(hwnd, lParam):
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value.lower()
            if any(k in title for k in ["copilot", "terminal", "cmd.exe", "powershell", "windows terminal"]):
                res.add(hwnd)
        return True
    
    ENUM_WINDOWS_PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    ctypes.windll.user32.EnumWindows(ENUM_WINDOWS_PROC(callback), 0)
    return res

def paste_text_to_hwnd(hwnd, text):
    """通过剪贴板 + Ctrl+V 绕开输入法问题"""
    if not hwnd: return
    
    # 强制激活
    ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    ps_cmd = (
        f"Set-Clipboard -Value '{text}'; "
        f"$wshell = New-Object -ComObject wscript.shell; "
        f"$wshell.SendKeys('{{ESC}}^v{{ENTER}}')"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd])

def main():
    # 1. 解析参数
    # 参数 1: 模型名称 (必填)
    # 参数 2: 目标文件夹 (选填)
    model_name = sys.argv[1] if len(sys.argv) > 1 else "gpt-4.1"
    target_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    print(f"--- Launching Copilot ({model_name}) ---")
    print(f"--- Folder: {target_dir} ---")
    
    # 锁文件路径
    lock_file = os.path.join(os.environ.get("TEMP", "."), "copilot_start.lock")
    
    # 互斥锁
    while os.path.exists(lock_file):
        if time.time() - os.path.getmtime(lock_file) > 15:
            try: os.remove(lock_file)
            except: pass
        else:
            time.sleep(0.1)
            
    try:
        with open(lock_file, "w") as f: f.write("locked")
        
        # 记录启动前的所有句柄
        before_hwnds = get_terminal_hwnds()
        
        # 启动新窗口，直接指定 target_dir
        subprocess.Popen(["wt", "-w", "-1", "-d", target_dir, "cmd", "/k", "copilot"])
        
        # 寻找差异句柄
        print("Waiting for window capture...")
        target_hwnd = None
        for _ in range(60):
            after_hwnds = get_terminal_hwnds()
            diff = after_hwnds - before_hwnds
            if diff:
                target_hwnd = list(diff)[0]
                break
            time.sleep(0.2)
        
        if not target_hwnd:
            print("Error: Capture failed.")
            return

        print(f"Captured handle: {target_hwnd}.")
        
    finally:
        if os.path.exists(lock_file):
            try: os.remove(lock_file)
            except: pass

    # 等待 copilot 加载并粘贴
    time.sleep(5) 
    paste_text_to_hwnd(target_hwnd, "/allow-all")
    time.sleep(2)
    paste_text_to_hwnd(target_hwnd, f"/model {model_name}")

if __name__ == "__main__":
    main()