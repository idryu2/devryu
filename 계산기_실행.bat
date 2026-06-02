@echo off
REM Windows 에서 더블클릭으로 계산기를 실행합니다.
cd /d "%~dp0"
python calculator.py
if errorlevel 1 (
    echo.
    echo [오류] Python 이 설치되어 있지 않거나 PATH 에 없습니다.
    echo https://www.python.org 에서 Python 을 설치한 뒤 다시 실행하세요.
    pause
)
