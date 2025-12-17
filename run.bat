@echo off
REM Quick runner for QR code generator

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Run the script with all arguments
python generate_qr_code_images.py %*

REM Keep window open if there was an error
if errorlevel 1 (
    pause
)
