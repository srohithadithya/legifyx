# ⚖️ LEGIFYX - AI-Powered Legal Contract Analysis Bot

<div align="center">

**AI-Powered Legal Assistant for Indian SMEs**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![Made in India](https://img.shields.io/badge/Made%20with%20❤️%20in-India-orange.svg)]()

*Empowering SME owners to understand complex contracts, identify legal risks, and receive actionable advice in plain language.*

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [♿ Accessibility](#-accessibility) • [📖 Usage](#-usage)

</div>

---

## 🎯 What is Legifyx?

**Legifyx** is a sophisticated GenAI-powered legal contract analysis bot designed specifically for Indian Small and Medium Enterprises (SMEs). It helps business owners:

- 📄 **Understand** complex legal documents in simple, plain language
- 🚨 **Identify** hidden risks and unfavorable terms before signing
- 💡 **Receive** actionable recommendations for contract improvements
- 🔒 **Ensure** compliance with Indian laws and regulations
- ♿ **Access** full voice navigation for visually impaired users

---

## ✨ Features

### 📊 Contract Analysis
| Feature | Description |
|---------|-------------|
| **Contract Classification** | Automatically identifies contract type (Employment, Vendor, Lease, NDA, etc.) |
| **Clause Extraction** | Extracts and categorizes individual clauses and sub-clauses |
| **Entity Recognition** | Identifies parties, dates, amounts, jurisdictions, and key terms |
| **Obligation Detection** | Distinguishes between obligations, rights, and prohibitions |

### 🚨 Risk Assessment
| Feature | Description |
|---------|-------------|
| **Clause-Level Scoring** | Rates each clause 1-10 for risk |
| **Contract-Level Score** | Composite risk score for the entire document |
| **Critical Clause Detection** | Identifies penalty, indemnity, termination, arbitration clauses |
| **Compliance Checking** | Verifies against Indian Contract Act, IT Act, and more |

### 🌐 Multilingual Support
- **English** (Primary)
- **Hindi** हिंदी
- **Tamil** தமிழ்
- **Telugu** తెలుగు
- **Kannada** ಕನ್ನಡ
- **Malayalam** മലയാളം
- **Marathi** मराठी
- **Gujarati** ગુજરાતી
- **Bengali** বাংলা
- **Punjabi** ਪੰਜਾਬੀ

### ♿ Accessibility Features
**Designed with visually impaired users in mind:**
- 🔊 **Voice Navigation** - Navigate the application using voice cues
- 📖 **Auto-Read Results** - Automatically speaks analysis findings
- 🎤 **Text-to-Speech** - Hear any content read aloud
- ⚡ **Adjustable Speech Rate** - Control voice speed (100-250 words/min)
- 🔊 **Voice Test** - Test TTS before using

### 📤 Export Options
- **PDF Reports** - Professional, branded analysis reports with risk summaries
- **JSON Data** - Structured data including analysis metadata, scores, and recommendations
- **Audio Summaries** - MP3 audio files of contract summaries in multiple languages

### 📚 Templates & Resources
- **Clause Templates** - 8 standard balanced clauses (Liability, Termination, Indemnity, etc.)
- **Contract Types** - 8 common SME contracts (Employment, Service, Vendor, NDA, etc.)
- **Legal Frameworks** - Information on 4 key Indian laws (Contract Act, Arbitration Act, IT Act, Consumer Protection)

### 🔒 Security & Privacy
- **AES-256 Encryption** - Sensitive data encrypted at rest
- **Audit Logging** - Complete trail of all actions
- **Local JSON Storage** - No external database required
- **Secure File Handling** - Proper cleanup of temporary files

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 - 3.12
- Windows / Linux / macOS

### Installation

```bash
# Clone the repository
git clone https://github.com/srohithadithya/legifyx.git
cd legifyx

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\\venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
```

### Running the Application

```bash
# Windows
run_legifyx.bat

# Linux/Mac
./run_legifyx.sh

# OR directly
streamlit run app.py --server.port 8501
```

Open your browser and navigate to: **http://localhost:8501**

---

## 📖 Usage

### 1. Upload Contract
- Click on **📤 Upload** tab
- Drag and drop or browse for your contract file
- Supported formats: PDF, DOCX, DOC, TXT, JPG, PNG
- Click **🔍 ANALYZE CONTRACT**

### 2. Review Results
- Navigate to **📊 Results** tab
- View overall risk score and classification
- Review critical issues and recommendations
- Read executive summary

### 3. Access Templates
- Go to **📚 Templates** tab
- Browse clause templates for reference
- View contract types available
- Learn about relevant Indian laws

### 4. Export Analysis
- In Results tab, click **📤 Export**
- Choose format:
  - **📄 Generate PDF** - Downloadable professional report
  - **📋 Download JSON** - Structured data export
  - **🔊 Generate Audio** - MP3 summary (requires gTTS)

### 5. View History
- Check **📜 History** tab
- See all previously analyzed contracts
- Review past risk scores
- Clear history if needed

---

## ♿ Accessibility Mode

Legifyx is designed to be accessible for visually impaired users:

### Enabling Accessibility Mode
1. Open the sidebar (left panel)
2. Toggle **\"🔊 Enable Accessibility Mode\"**
3. Configure options:
   - ✅ **Voice Navigation** - Hear navigation announcements
   - ✅ **Auto-Read Results** - Automatically read analysis findings
   - 🔈 **Voice Speed** - Adjust speech rate (100-250)
   - 🔊 **Test Voice** - Verify TTS is working

### Using Voice Features
- Use **🎤** buttons throughout the app to hear content
- Analysis results can be auto-read when enabled
- Export audio summaries for offline listening

---

## 📁 Project Structure

```
legifyx/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── run_legifyx.bat                 # Windows launcher
├── .gitignore                      # Git ignore rules
│
├── config/
│   └── settings.py                 # Application configuration
│
├── core/
│   ├── analyzer.py                 # Contract analysis orchestrator
│   ├── nlp_engine.py               # NLP processing engine
│   ├── risk_scorer.py              # Risk assessment module
│   └── entity_extractor.py         # Named entity extraction
│
├── services/
│   ├── document_parser.py          # PDF, DOCX, TXT, Image parsing
│   ├── ocr_service.py              # Image OCR processing
│   ├── translation.py              # Multilingual translation
│   └── tts_service.py              # Text-to-speech accessibility
│
├── templates/
│   └── clause_templates.py         # Standard clause templates
│
├── utils/
│   ├── pdf_generator.py            # PDF report generation
│   ├── audit_logger.py             # Audit trail logging
│   └── encryption.py               # Data encryption utilities
│
├── data/
│   ├── knowledge_base.py           # SME knowledge base
│   └── storage/                    # JSON storage directory
│
├── exports/                        # Generated PDF reports
├── audio_output/                   # Generated audio files
│
└── samples/
    └── sample_service_agreement.txt # Sample contract for testing
```

---

## 🛡️ Compliance & Legal Framework

Legifyx references key Indian legal frameworks:

| Law/Regulation | Coverage |
|----------------|----------|
| **Indian Contract Act, 1872** | Contract validity, enforceability, lawful consideration |
| **Arbitration and Conciliation Act, 1996** | Dispute resolution clauses, arbitration agreements |
| **Information Technology Act, 2000** | E-contracts, digital signatures, data protection |
| **Consumer Protection Act, 2019** | Unfair contract terms, consumer rights |

---

## 📋 Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Standard PDF documents |
| Word | `.docx`, `.doc` | Microsoft Word documents |
| Text | `.txt` | Plain text files |
| Images | `.jpg`, `.png` | Scanned documents (requires Tesseract OCR) |

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):

```env
# Application Settings
APP_ENV=production
DEBUG=false

# File Limits
MAX_FILE_SIZE_MB=50

# OCR Settings (if Tesseract installed separately)
TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
```

### Storage
- Analysis history stored in: `data/storage/history.json`
- PDF reports saved to: `exports/`
- Audio files saved to: `audio_output/`

---

## 🔍 How It Works

1. **Document Parsing**: Extracts text from uploaded files using PyPDF2, python-docx, pdfplumber, and Tesseract OCR
2. **NLP Processing**: Uses spaCy for tokenization, entity recognition, and clause extraction
3. **Risk Analysis**: Scores clauses based on keywords, patterns, and legal frameworks
4. **Report Generation**: Creates formatted reports using ReportLab
5. **Audio Generation**: Converts text to speech using pyttsx3 (local) and gTTS (files)

---

## 📦 Dependencies

Key packages:
- **streamlit** - Web interface
- **spacy** - NLP engine
- **nltk** - Natural language toolkit
- **PyPDF2** - PDF parsing
- **python-docx** - Word document parsing
- **pdfplumber** - Advanced PDF extraction
- **Pillow** - Image processing
- **pytesseract** - OCR (optional)
- **pyttsx3** - Text-to-speech (local)
- **gTTS** - Text-to-speech (MP3 files)
- **deep-translator** - Translation service
- **reportlab** - PDF generation
- **cryptography** - Encryption utilities

---

## 🐛 Troubleshooting

### Voice Not Working
- Install: `pip install pyttsx3 gTTS`
- Windows: Ensure Microsoft Speech API is available
- macOS: Use `say` command fallback
- Linux: Install `espeak`: `sudo apt-get install espeak`

### OCR Not Working
- Install Tesseract: https://github.com/tesseract-ocr/tesseract
- Add to PATH or set `TESSERACT_PATH` in `.env`

### PDF Generation Failing
- Ensure ReportLab is installed: `pip install reportlab`
- Check write permissions in `exports/` folder

---

## 🙏 Acknowledgments

- **spaCy** - Industrial-strength NLP
- **NLTK** - Natural Language Toolkit
- **Streamlit** - Beautiful web applications
- **ReportLab** - PDF generation
- **Google TTS** - Text-to-speech service

---

## 📞 Support

For support or questions:
- 📧 Email: support@legifyx.com
- 🐛 Issues: https://github.com/srohithadithya/legifyx/issues

---

<div align="center">

**Made with ❤️ for Indian SMEs**

⚖️ **LEGIFYX** - *Simplifying Legal Complexity*

© 2026 Legifyx. All Rights Reserved.

</div>
