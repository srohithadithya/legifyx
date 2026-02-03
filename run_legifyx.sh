#!/bin/bash

echo "========================================"
echo "       LEGIFYX - Contract Analysis Bot"
echo "       AI-Powered Legal Assistant"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! pip show streamlit > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo "Downloading NLP models..."
    python -m spacy download en_core_web_sm
    python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
fi

echo ""
echo "Starting Legifyx..."
echo ""
echo "Open your browser and navigate to: http://localhost:8501"
echo ""

streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
