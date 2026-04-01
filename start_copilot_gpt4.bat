@echo off
:: %~dp0 代表当前 .bat 所在的目录路径
python "%~dp0start_copilot.py" gpt-4.1 "%1"
pause
