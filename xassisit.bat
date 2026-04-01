@echo off
:: 使用现有的 xassisit.py 处理监听逻辑
echo Starting xassisit.py...
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%xassisit.py" gpt-4.1 "%SCRIPT_DIR%."
echo.
echo Exit code: %ERRORLEVEL%
pause
