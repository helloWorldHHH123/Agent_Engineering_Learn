@echo off
setlocal
set "PYTHON=E:\Document\BeiFen\AIClass\Anaconda3Virtual\conda\envs\AgentPy311\python.exe"

if not exist "%PYTHON%" (
    echo ERROR: Python not found at:
    echo %PYTHON%
    pause
    exit /b 1
)

echo === Target Python ===
"%PYTHON%" --version
if errorlevel 1 goto :failed

echo.
echo === Installing Agent packages ===
"%PYTHON%" -m pip install openai-agents python-dotenv requests httpx deepseek-tokenizer
if errorlevel 1 goto :failed

echo.
echo === Checking key imports ===
"%PYTHON%" -c "import agents, openai, dotenv, requests, httpx, json; print('Main packages imported successfully; json is built in.')"
if errorlevel 1 goto :failed

echo.
echo Installation finished.
pause
exit /b 0

:failed
echo.
echo Installation or validation failed. Review the error above.
pause
exit /b 1
