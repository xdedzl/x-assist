@echo off

:: Use hardcoded paths for absolute reliability
set PY=python.exe
set SCRIPT=D:\Projects\x-assist\start_copilot.py

echo.
echo Installing Context Menu (Hardcoded Paths)...
echo.

:: Directory Background (Empty space)
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist" /v "MUIVerb" /t REG_SZ /d "XAssist" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist" /v "SubCommands" /t REG_SZ /d "" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist" /v "Icon" /t REG_SZ /d "shell32.dll,22" /f

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist\shell\GPT4" /v "MUIVerb" /t REG_SZ /d "copilot-gpt-4.1" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist\shell\GPT4\command" /v "" /t REG_SZ /d "%PY% \"%SCRIPT%\" gpt-4.1 \"%%V\"" /f

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist\shell\Sonnet" /v "MUIVerb" /t REG_SZ /d "copilot-claude-sonnet-4.6" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist\shell\Sonnet\command" /v "" /t REG_SZ /d "%PY% \"%SCRIPT%\" claude-sonnet-4.6 \"%%V\"" /f

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist\shell\Opus" /v "MUIVerb" /t REG_SZ /d "copilot-claude-opus-4.6" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\XAssist\shell\Opus\command" /v "" /t REG_SZ /d "%PY% \"%SCRIPT%\" claude-opus-4.6 \"%%V\"" /f


:: Directory Icon
reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist" /v "MUIVerb" /t REG_SZ /d "XAssist" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist" /v "SubCommands" /t REG_SZ /d "" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist" /v "Icon" /t REG_SZ /d "shell32.dll,22" /f

reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist\shell\GPT4" /v "MUIVerb" /t REG_SZ /d "copilot-gpt-4.1" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist\shell\GPT4\command" /v "" /t REG_SZ /d "%PY% \"%SCRIPT%\" gpt-4.1 \"%%V\"" /f

reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist\shell\Sonnet" /v "MUIVerb" /t REG_SZ /d "copilot-claude-sonnet-4.6" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist\shell\Sonnet\command" /v "" /t REG_SZ /d "%PY% \"%SCRIPT%\" claude-sonnet-4.6 \"%%V\"" /f

reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist\shell\Opus" /v "MUIVerb" /t REG_SZ /d "copilot-claude-opus-4.6" /f
reg add "HKEY_CLASSES_ROOT\Directory\shell\XAssist\shell\Opus\command" /v "" /t REG_SZ /d "%PY% \"%SCRIPT%\" claude-opus-4.6 \"%%V\"" /f

echo.
echo Success. Please test context menu.
pause
