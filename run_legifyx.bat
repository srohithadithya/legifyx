@echo off
echo ========================================
echo        LEGIFYX - Contract Analysis Bot
echo        AI-Powered Legal Assistant
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    
    echo Downloading NLP models...
    python -m spacy download en_core_web_sm
    python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
)

echo.
echo Starting Legifyx...
echo.
echo Open your browser and navigate to: http://localhost:8501
echo.

streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
