@echo off
REM Build and run the project locally on Windows

echo Building Sherlock...

REM Create virtual environment
python -m venv venv

REM Activate
call venv\Scripts\activate.bat

REM Install dependencies
pip install -q -r backend\requirements.txt

REM Run tests
echo Running tests...
pytest test_api.py -v

echo.
echo Setup complete! To start the backend:
echo   venv\Scripts\activate.bat
echo   cd backend && python app/main.py
