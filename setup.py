"""
Legifyx Setup Script
Initializes the environment and downloads required models
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - Success")
        if result.stdout:
            print(result.stdout[:500])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr[:500] if e.stderr else str(e)}")
        return False


def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║     ⚖️  LEGIFYX - Setup Script                             ║
    ║     AI-Powered Legal Contract Analysis Bot                 ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Create required directories
    directories = [
        "data/notifications",
        "data/knowledge_base",
        "logs",
        "uploads",
        "exports",
        "audio_output"
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    # Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n⚠️  Some dependencies failed to install. The app may not work correctly.")
    
    # Download spaCy model
    print("\n📚 Downloading NLP models...")
    
    run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading spaCy English model (small)"
    )
    
    # Try to download large model (optional)
    run_command(
        f"{sys.executable} -m spacy download en_core_web_lg",
        "Downloading spaCy English model (large) - Optional"
    )
    
    # Download NLTK data
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("   ✅ NLTK data downloaded")
    except Exception as e:
        print(f"   ⚠️ NLTK download failed: {e}")
    
    # Check for Tesseract
    print("\n🔍 Checking for Tesseract OCR...")
    try:
        result = subprocess.run(
            "tesseract --version",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("   ✅ Tesseract is installed")
            print(f"   Version: {result.stdout.split()[1] if result.stdout else 'Unknown'}")
        else:
            raise Exception("Not found")
    except:
        print("   ⚠️ Tesseract not found. OCR features will be limited.")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Final summary
    print("""
    
    ╔════════════════════════════════════════════════════════════╗
    ║                   🎉 Setup Complete!                       ║
    ╠════════════════════════════════════════════════════════════╣
    ║                                                            ║
    ║  To start Legifyx:                                         ║
    ║                                                            ║
    ║  Windows:  run_legifyx.bat                                 ║
    ║            OR                                              ║
    ║            streamlit run app.py                            ║
    ║                                                            ║
    ║  Linux/Mac: ./run_legifyx.sh                               ║
    ║             OR                                             ║
    ║             streamlit run app.py                           ║
    ║                                                            ║
    ║  Open http://localhost:8501 in your browser                ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
