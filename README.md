# 🏛️ Legifyx - AI-Powered Legal Contract Analysis Platform

<p align="center">
  <img src="assets/logo.png" alt="Legifyx Logo" width="200"/>
</p>

<p align="center">
  <strong>Empowering SMEs with Intelligent Contract Analysis & Risk Assessment</strong>
</p>

---

## 🎯 Overview

**Legifyx** is a sophisticated GenAI-powered legal assistant designed specifically for Small and Medium Business (SME) owners in India. It helps understand complex contracts, identify potential legal risks, and receive actionable advice in plain language.

## ✨ Key Features

### 📄 Contract Analysis
- **Multi-format Support**: PDF, DOC/DOCX, TXT, and live image scanning
- **Contract Type Classification**: Employment, Vendor, Lease, Partnership, Service contracts
- **Clause & Sub-Clause Extraction**: Intelligent parsing of contract structure
- **Named Entity Recognition**: Parties, Dates, Jurisdiction, Liabilities, Amounts

### ⚖️ Risk Assessment
- **Clause-level Risk Scores**: Low / Medium / High ratings
- **Contract-level Composite Risk Score**: Overall risk evaluation
- **Critical Clause Detection**:
  - Penalty Clauses
  - Indemnity Clauses
  - Unilateral Termination
  - Arbitration & Jurisdiction Terms
  - Auto-Renewal & Lock-in Periods
  - Non-compete & IP Transfer Clauses

### 🔍 NLP Capabilities
- Obligation vs. Right vs. Prohibition Identification
- Risk & Compliance Detection
- Ambiguity Detection & Flagging
- Clause Similarity Matching to Standard Templates

### 🌐 Multilingual Support
- English + Pan-India Languages (Hindi, Tamil, Telugu, etc.)
- Internal normalization for NLP processing
- Output in simple business English or regional languages
- **Text-to-Speech** for accessibility (visually impaired users)

### 📊 User-Facing Outputs
- Simplified contract summary
- Clause-by-clause plain-language explanation
- Unfavorable clause highlighting
- Suggested renegotiation alternatives
- Standardized SME-friendly contract templates
- PDF export for legal review

### 🔒 Security & Privacy
- End-to-end data encryption
- Local processing (no external APIs)
- Audit trail logging
- GDPR-compliant data handling
- Secure session management

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **NLP Engine** | Python, spaCy, NLTK |
| **AI/ML** | Transformers, Sentence-BERT |
| **UI Framework** | Streamlit |
| **Document Processing** | PyPDF2, python-docx, Tesseract OCR |
| **Storage** | Local file system, JSON audit logs |
| **Text-to-Speech** | pyttsx3, gTTS |
| **PDF Generation** | ReportLab, WeasyPrint |

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.9+
pip (Python package manager)
Tesseract OCR (for image scanning)
```

### Installation

1. Clone the repository:
```bash
cd legifyx
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy models:
```bash
python -m spacy download en_core_web_lg
```

5. Run the application:
```bash
streamlit run app.py
```

## 📁 Project Structure

```
legifyx/
├── app.py                          # Main Streamlit application
├── setup.py                        # Setup and initialization script
├── requirements.txt                # Python dependencies
├── run_legifyx.bat                 # Windows launcher
├── run_legifyx.sh                  # Linux/Mac launcher
├── project.json                    # Project metadata
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore rules
│
├── config/
│   └── settings.py                 # Application configuration
│
├── core/
│   ├── __init__.py
│   ├── analyzer.py                 # Contract analysis orchestrator
│   ├── nlp_engine.py               # NLP processing engine
│   ├── risk_scorer.py              # Risk assessment module
│   └── entity_extractor.py         # Named entity extraction
│
├── services/
│   ├── __init__.py
│   ├── document_parser.py          # PDF, DOCX, TXT parsing
│   ├── ocr_service.py              # Image OCR processing
│   ├── translation.py              # Multilingual translation
│   ├── tts_service.py              # Text-to-speech accessibility
│   └── notification_service.py     # Real-time notifications
│
├── templates/
│   ├── clause_templates.py         # Standard clause templates
│   └── contract_templates/         # Full contract templates
│
├── utils/
│   ├── __init__.py
│   ├── pdf_generator.py            # PDF report generation
│   ├── audit_logger.py             # Audit trail logging
│   └── encryption.py               # Data encryption utilities
│
├── data/
│   ├── __init__.py
│   └── knowledge_base.py           # SME knowledge base
│
├── assets/
│   ├── logo.png                    # Legifyx brand logo
│   └── styles.css                  # Custom UI styling
│
├── samples/
│   └── sample_service_agreement.txt # Sample contract for testing
│
├── logs/                           # Application logs
├── uploads/                        # Uploaded documents
└── exports/                        # Generated reports
```

## 📜 License

This project is proprietary software developed for SME legal assistance.

## 📞 Support

For support and inquiries, please contact the Legifyx team.

---

<p align="center">
  <strong>Built with ❤️ for Indian SMEs</strong>
</p>
