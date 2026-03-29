"""
Legifyx Configuration Settings
Centralized configuration for the entire application
"""

import os
from pathlib import Path
from datetime import datetime

# Base Paths
BASE_DIR = Path(__file_).parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"
UPLOADS_DIR = BASE_DIR / "uploads"
EXPORTS_DIR = BASE_DIR / "exports"

# Create directories if they don't exist
for directory in [DATA_DIR, TEMPLATES_DIR, ASSETS_DIR, LOGS_DIR, UPLOADS_DIR, EXPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application Settings
APP_NAME = "Legifyx"
APP_VERSION = "1.0.0"
APP_TAGLINE = "AI-Powered Legal Contract Analysis"

# Brand Colors
BRAND_COLORS = {
    "primary": "#1E3A5F",      # Deep Navy Blue
    "secondary": "#C9A227",     # Gold
    "accent": "#2E7D32",        # Legal Green
    "danger": "#C62828",        # Risk Red
    "warning": "#F9A825",       # Caution Yellow
    "success": "#2E7D32",       # Success Green
    "background": "#0A1628",    # Dark Background
    "surface": "#1A2942",       # Card Background
    "text_primary": "#FFFFFF",  # White Text
    "text_secondary": "#B0BEC5" # Gray Text
}

# Risk Score Thresholds
RISK_THRESHOLDS = {
    "low": (0, 3.9),
    "medium": (4.0, 6.9),
    "high": (7.0, 10.0)
}

# Contract Types
CONTRACT_TYPES = [
    "Employment Agreement",
    "Vendor Contract",
    "Lease Agreement",
    "Partnership Deed",
    "Service Contract",
    "Non-Disclosure Agreement",
    "Franchise Agreement",
    "Distribution Agreement",
    "Consulting Agreement",
    "License Agreement",
    "Joint Venture Agreement",
    "Supply Agreement",
    "Maintenance Contract",
    "Agency Agreement",
    "Other"
]

# Critical Clause Categories
CRITICAL_CLAUSES = {
    "penalty": {
        "name": "Penalty Clauses",
        "risk_weight": 0.15,
        "keywords": ["penalty", "fine", "damages", "liquidated damages", "forfeit", "compensation"]
    },
    "indemnity": {
        "name": "Indemnity Clauses",
        "risk_weight": 0.15,
        "keywords": ["indemnify", "indemnification", "hold harmless", "defend", "liability"]
    },
    "termination": {
        "name": "Unilateral Termination",
        "risk_weight": 0.12,
        "keywords": ["terminate", "termination", "cancel", "breach", "default", "notice period"]
    },
    "arbitration": {
        "name": "Arbitration & Jurisdiction",
        "risk_weight": 0.10,
        "keywords": ["arbitration", "jurisdiction", "governing law", "dispute resolution", "mediation"]
    },
    "renewal": {
        "name": "Auto-Renewal & Lock-in",
        "risk_weight": 0.12,
        "keywords": ["auto-renewal", "automatic renewal", "lock-in", "minimum term", "commitment period"]
    },
    "non_compete": {
        "name": "Non-compete Clauses",
        "risk_weight": 0.13,
        "keywords": ["non-compete", "non-competition", "restrictive covenant", "exclusivity"]
    },
    "ip_transfer": {
        "name": "IP Transfer Clauses",
        "risk_weight": 0.13,
        "keywords": ["intellectual property", "IP rights", "patent", "copyright", "trademark", "ownership transfer"]
    },
    "confidentiality": {
        "name": "Confidentiality & NDA",
        "risk_weight": 0.10,
        "keywords": ["confidential", "confidentiality", "non-disclosure", "trade secret", "proprietary"]
    }
}

# Entity Types for Extraction
ENTITY_TYPES = [
    "PARTY",           # Contract parties
    "DATE",            # Important dates
    "AMOUNT",          # Financial amounts
    "DURATION",        # Time periods
    "JURISDICTION",    # Legal jurisdiction
    "OBLIGATION",      # Obligations
    "RIGHT",           # Rights
    "PROHIBITION",     # Prohibitions
    "DELIVERABLE",     # Deliverables
    "METRIC",          # Performance metrics
    "TERMINATION",     # Termination conditions
    "IP_ASSET"         # Intellectual property assets
]

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "gu": "Gujarati",
    "bn": "Bengali",
    "pa": "Punjabi"
}

# Document Settings
MAX_FILE_SIZE_MB = 50
ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png"]

# OCR Settings
OCR_LANGUAGES = "eng+hin"
OCR_DPI = 300

# Text-to-Speech Settings
TTS_RATE = 150
TTS_VOLUME = 0.9

# Audit Log Settings
AUDIT_LOG_FILE = LOGS_DIR / "audit_log.json"
MAX_AUDIT_ENTRIES = 10000

# Security Settings
ENCRYPTION_KEY_FILE = BASE_DIR / ".encryption_key"
SESSION_TIMEOUT_MINUTES = 60

# PDF Export Settings
PDF_SETTINGS = {
    "page_size": "A4",
    "margin_top": 50,
    "margin_bottom": 50,
    "margin_left": 50,
    "margin_right": 50,
    "font_family": "Helvetica",
    "font_size": 11,
    "header_font_size": 16,
    "line_height": 14
}

# Risk Indicators for Indian Law Compliance
INDIAN_LAW_COMPLIANCE_CHECKS = {
    "stamp_duty": {
        "name": "Stamp Duty Compliance",
        "description": "Check for stamp duty requirements under Indian Stamp Act"
    },
    "registration": {
        "name": "Registration Requirements",
        "description": "Verify if contract requires registration under Registration Act"
    },
    "arbitration_act": {
        "name": "Arbitration Act Compliance",
        "description": "Check compliance with Arbitration and Conciliation Act, 1996"
    },
    "contract_act": {
        "name": "Indian Contract Act",
        "description": "Verify compliance with Indian Contract Act, 1872"
    },
    "it_act": {
        "name": "IT Act Compliance",
        "description": "Check for IT Act, 2000 requirements for electronic contracts"
    }
}

# Standard Template Categories
TEMPLATE_CATEGORIES = [
    "Employment",
    "Vendor & Supply",
    "Lease & Rental",
    "Partnership",
    "Service & Consulting",
    "NDA & Confidentiality",
    "Franchise",
    "Distribution",
    "License",
    "Joint Venture"
]
