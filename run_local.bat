@echo off
echo Setting up environment for Daily Life Helper API...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.9 or higher.
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the application
echo Starting the application...
echo.
echo Access the API at http://localhost:8000
echo API documentation is available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn app:app --reload

REM Deactivate virtual environment on exit
call venv\Scripts\deactivate