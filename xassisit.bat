@echo off
:: 在新的 Windows Terminal 窗口中启动 xassisit.py
:: copilot 将在新 wt 窗口内通过 ConPTY 运行，脚本可捕获全部输出
set "SCRIPT_DIR=%~dp0"
set "TARGET_DIR=%~1"
if "%TARGET_DIR%"=="" set "TARGET_DIR=%SCRIPT_DIR%."
wt -w 0 nt -d "%TARGET_DIR%" --title "Copilot Assistant" -- python "%SCRIPT_DIR%xassisit.py" gpt-4.1 "%TARGET_DIR%"
