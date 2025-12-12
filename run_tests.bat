@echo off
echo Running SwissAxa Portal Tests...
echo.
call venv\Scripts\activate.bat
python run_tests.py
pause

