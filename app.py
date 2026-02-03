"""
Legifyx - AI-Powered Legal Contract Analysis Bot
Premium Professional Interface with Accessibility Features

A sophisticated GenAI-powered legal assistant for SME owners
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import hashlib
import base64

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import (
    APP_NAME, APP_VERSION, APP_TAGLINE, BRAND_COLORS,
    CONTRACT_TYPES, SUPPORTED_LANGUAGES, CRITICAL_CLAUSES
)
from core.analyzer import ContractAnalyzer
from core.risk_scorer import RiskLevel
from services.document_parser import DocumentParser
from services.translation import TranslationService
from services.tts_service import TTSService
from utils.pdf_generator import PDFGenerator
from utils.audit_logger import AuditLogger
from utils.encryption import EncryptionService

# Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} - Legal Contract Analysis Bot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_premium_css():
    """Load premium professional CSS styling"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
        
        /* Root Variables */
        :root {
            --primary: #0F2644;
            --primary-light: #1A3A5C;
            --secondary: #D4AF37;
            --secondary-light: #E8C547;
            --accent: #00A878;
            --danger: #DC3545;
            --warning: #FFC107;
            --success: #28A745;
            --dark: #0A1929;
            --surface: #132F4C;
            --text-primary: #FFFFFF;
            --text-secondary: #B0BEC5;
            --border: rgba(212, 175, 55, 0.2);
        }
        
        /* Main Background */
        .stApp {
            background: linear-gradient(135deg, #0A1929 0%, #0F2644 50%, #132F4C 100%);
        }
        
        .main .block-container {
            padding-top: 2rem;
            max-width: 1400px;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Premium Header */
        .premium-header {
            background: linear-gradient(135deg, rgba(15, 38, 68, 0.95) 0%, rgba(26, 58, 92, 0.95) 100%);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
        }
        
        .brand-name {
            font-family: 'Playfair Display', serif;
            font-size: 4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #D4AF37 0%, #F4E4A6 50%, #D4AF37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 8px;
            margin-bottom: 10px;
            text-shadow: 0 0 60px rgba(212, 175, 55, 0.5);
        }
        
        .brand-icon {
            font-size: 3rem;
            margin-right: 15px;
        }
        
        .brand-tagline {
            font-family: 'Inter', sans-serif;
            color: #B0BEC5;
            font-size: 1.2rem;
            font-weight: 300;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        
        .brand-badge {
            display: inline-block;
            background: linear-gradient(135deg, #D4AF37 0%, #E8C547 100%);
            color: #0A1929;
            padding: 8px 20px;
            border-radius: 30px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 2px;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        }
        
        /* Professional Cards */
        .pro-card {
            background: linear-gradient(145deg, rgba(19, 47, 76, 0.9) 0%, rgba(15, 38, 68, 0.9) 100%);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .pro-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            border-color: rgba(212, 175, 55, 0.4);
        }
        
        .card-title {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #D4AF37;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Risk Score Display */
        .risk-gauge {
            background: linear-gradient(145deg, #132F4C 0%, #0F2644 100%);
            border: 2px solid var(--border);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .risk-gauge::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
        }
        
        .risk-score-big {
            font-family: 'Inter', sans-serif;
            font-size: 5rem;
            font-weight: 800;
            line-height: 1;
            position: relative;
            z-index: 1;
        }
        
        .risk-low { color: #28A745; text-shadow: 0 0 30px rgba(40, 167, 69, 0.5); }
        .risk-medium { color: #FFC107; text-shadow: 0 0 30px rgba(255, 193, 7, 0.5); }
        .risk-high { color: #FF9800; text-shadow: 0 0 30px rgba(255, 152, 0, 0.5); }
        .risk-critical { color: #DC3545; text-shadow: 0 0 30px rgba(220, 53, 69, 0.5); }
        
        .risk-label {
            font-size: 1.5rem;
            color: #B0BEC5;
            margin-top: 10px;
            font-weight: 300;
        }
        
        .risk-badge {
            display: inline-block;
            padding: 12px 30px;
            border-radius: 50px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-top: 20px;
            font-size: 0.9rem;
        }
        
        .badge-low { background: rgba(40, 167, 69, 0.2); color: #28A745; border: 2px solid #28A745; }
        .badge-medium { background: rgba(255, 193, 7, 0.2); color: #FFC107; border: 2px solid #FFC107; }
        .badge-high { background: rgba(255, 152, 0, 0.2); color: #FF9800; border: 2px solid #FF9800; }
        .badge-critical { background: rgba(220, 53, 69, 0.2); color: #DC3545; border: 2px solid #DC3545; }
        
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(145deg, #1A3A5C 0%, #132F4C 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: scale(1.05);
            border-color: #D4AF37;
        }
        
        .metric-value {
            font-family: 'Inter', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            color: #D4AF37;
            line-height: 1;
        }
        
        .metric-label {
            font-size: 0.8rem;
            color: #B0BEC5;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 10px;
            font-weight: 500;
        }
        
        /* Upload Area */
        .upload-zone {
            background: linear-gradient(145deg, rgba(19, 47, 76, 0.8) 0%, rgba(15, 38, 68, 0.8) 100%);
            border: 3px dashed rgba(212, 175, 55, 0.4);
            border-radius: 20px;
            padding: 50px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .upload-zone:hover {
            border-color: #D4AF37;
            background: rgba(212, 175, 55, 0.05);
        }
        
        .upload-icon {
            font-size: 4rem;
            margin-bottom: 20px;
        }
        
        .upload-text {
            font-size: 1.2rem;
            color: #FFFFFF;
            font-weight: 500;
        }
        
        .upload-subtext {
            font-size: 0.9rem;
            color: #B0BEC5;
            margin-top: 10px;
        }
        
        /* Clause Cards */
        .clause-card {
            background: rgba(19, 47, 76, 0.7);
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            border-left: 5px solid #D4AF37;
            transition: all 0.3s ease;
        }
        
        .clause-card:hover {
            transform: translateX(5px);
            background: rgba(26, 58, 92, 0.8);
        }
        
        .clause-critical {
            border-left-color: #DC3545;
            background: rgba(220, 53, 69, 0.1);
        }
        
        .clause-warning {
            border-left-color: #FFC107;
            background: rgba(255, 193, 7, 0.1);
        }
        
        .clause-safe {
            border-left-color: #28A745;
            background: rgba(40, 167, 69, 0.1);
        }
        
        /* Recommendations */
        .recommendation-item {
            background: linear-gradient(90deg, rgba(40, 167, 69, 0.1) 0%, transparent 100%);
            border-left: 4px solid #28A745;
            padding: 15px 20px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }
        
        .recommendation-item:hover {
            background: linear-gradient(90deg, rgba(40, 167, 69, 0.2) 0%, transparent 100%);
            transform: translateX(5px);
        }
        
        /* Accessibility Panel */
        .accessibility-panel {
            background: linear-gradient(145deg, #1A3A5C 0%, #132F4C 100%);
            border: 2px solid #00A878;
            border-radius: 16px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .accessibility-title {
            color: #00A878;
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #D4AF37 0%, #E8C547 100%);
            color: #0A1929;
            border: none;
            border-radius: 50px;
            padding: 15px 40px;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.5);
        }
        
        /* Section Headers */
        .section-header {
            font-family: 'Inter', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 30px 0 20px 0;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .section-icon {
            font-size: 1.5rem;
        }
        
        /* Info Boxes */
        .info-box {
            background: rgba(0, 168, 120, 0.1);
            border: 1px solid rgba(0, 168, 120, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
        }
        
        .warning-box {
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
        }
        
        .danger-box {
            background: rgba(220, 53, 69, 0.1);
            border: 1px solid rgba(220, 53, 69, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
        }
        
        /* Sidebar Styling */
        .css-1d391kg, [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F2644 0%, #0A1929 100%);
        }
        
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: rgba(26, 58, 92, 0.6);
            border-radius: 10px;
            font-weight: 600;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(26, 58, 92, 0.6);
            border-radius: 10px 10px 0 0;
            padding: 12px 25px;
            font-weight: 600;
            color: #B0BEC5;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #D4AF37 0%, #E8C547 100%);
            color: #0A1929;
        }
        
        /* Progress */
        .stProgress > div > div {
            background: linear-gradient(90deg, #D4AF37 0%, #E8C547 100%);
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: rgba(19, 47, 76, 0.5);
            border: 2px dashed rgba(212, 175, 55, 0.3);
            border-radius: 16px;
            padding: 20px;
        }
        
        /* Voice Button */
        .voice-btn {
            background: linear-gradient(135deg, #00A878 0%, #00C896 100%);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 25px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        
        .voice-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0, 168, 120, 0.4);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: #0A1929; }
        ::-webkit-scrollbar-thumb { background: #D4AF37; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #E8C547; }
        
        /* Status Indicators */
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: blink 1.5s infinite;
        }
        
        .status-active { background: #28A745; }
        .status-warning { background: #FFC107; }
        .status-danger { background: #DC3545; }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .brand-name { font-size: 2.5rem; letter-spacing: 3px; }
            .brand-tagline { font-size: 0.9rem; }
            .risk-score-big { font-size: 3.5rem; }
        }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'analysis_result': None,
        'uploaded_file_name': None,
        'contract_text': None,
        'analysis_history': [],
        'accessibility_mode': False,
        'voice_enabled': False,
        'high_contrast': False,
        'large_text': False,
        'auto_read': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_premium_header():
    """Render the premium professional header"""
    st.markdown("""
    <div class="premium-header">
        <div class="brand-name">
            <span class="brand-icon">⚖️</span>LEGIFYX
        </div>
        <div class="brand-tagline">AI-Powered Legal Contract Analysis Bot</div>
        <div class="brand-badge">🛡️ ENTERPRISE GRADE • SECURE • TRUSTED</div>
    </div>
    """, unsafe_allow_html=True)


def render_accessibility_sidebar():
    """Render accessibility options in sidebar"""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 2rem;">⚖️</div>
            <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: #D4AF37; font-weight: 700;">LEGIFYX</div>
            <div style="font-size: 0.7rem; color: #B0BEC5; letter-spacing: 2px;">LEGAL AI ASSISTANT</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Accessibility Section
        st.markdown("""
        <div class="accessibility-title">
            ♿ Accessibility Options
        </div>
        """, unsafe_allow_html=True)
        
        # Enable accessibility mode
        accessibility_mode = st.checkbox(
            "🔊 Enable Accessibility Mode",
            value=st.session_state.accessibility_mode,
            help="Enable voice assistance and screen reader optimization for visually impaired users"
        )
        st.session_state.accessibility_mode = accessibility_mode
        
        if accessibility_mode:
            st.success("✅ Accessibility Mode Active")
            
            # Voice options
            st.session_state.voice_enabled = st.checkbox(
                "🎤 Voice Navigation",
                value=st.session_state.voice_enabled,
                help="Enable voice-guided navigation"
            )
            
            st.session_state.auto_read = st.checkbox(
                "📖 Auto-Read Results",
                value=st.session_state.auto_read,
                help="Automatically read analysis results aloud"
            )
            
            # Voice speed
            voice_speed = st.slider(
                "🔈 Voice Speed",
                min_value=100,
                max_value=250,
                value=150,
                step=25,
                help="Adjust text-to-speech speed"
            )
            
            st.session_state.high_contrast = st.checkbox(
                "🔆 High Contrast Mode",
                value=st.session_state.high_contrast
            )
            
            st.session_state.large_text = st.checkbox(
                "🔤 Large Text Mode",
                value=st.session_state.large_text
            )
        else:
            voice_speed = 150
        
        st.markdown("---")
        
        # Language Selection
        st.markdown("### 🌐 Language Settings")
        output_language = st.selectbox(
            "Output Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x],
            index=0
        )
        
        st.markdown("---")
        
        # Session Stats
        st.markdown("### 📊 Session Statistics")
        analyses_count = len(st.session_state.get('analysis_history', []))
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{analyses_count}</div>
            <div class="metric-label">Contracts Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Version Info
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0; color: #B0BEC5; font-size: 0.75rem;">
            <div>Version {APP_VERSION}</div>
            <div style="margin-top: 5px;">🔒 Secure & Encrypted</div>
        </div>
        """, unsafe_allow_html=True)
        
        return {
            'output_language': output_language,
            'accessibility_mode': accessibility_mode,
            'voice_enabled': st.session_state.voice_enabled if accessibility_mode else False,
            'auto_read': st.session_state.auto_read if accessibility_mode else False,
            'voice_speed': voice_speed
        }


def speak_text(text: str, rate: int = 150):
    """Speak text using TTS service"""
    try:
        tts = TTSService()
        tts.set_voice_properties(rate=rate)
        tts.speak(text)
    except Exception as e:
        st.warning(f"Voice output unavailable: {e}")


def render_upload_section(settings):
    """Render the professional upload section"""
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📄</span>
        Upload Contract Document
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Drop your contract file here or click to browse",
            type=['pdf', 'docx', 'doc', 'txt', 'jpg', 'jpeg', 'png'],
            help="Supported formats: PDF, Word Documents, Text Files, and Images"
        )
        
        if settings['accessibility_mode'] and settings['voice_enabled']:
            if st.button("🎤 Voice: Describe Upload Options"):
                speak_text(
                    "Upload section. You can upload PDF documents, Word files, text files, or images of contracts. "
                    "Click the upload button or drag and drop your file.",
                    settings['voice_speed']
                )
    
    with col2:
        st.markdown("""
        <div class="pro-card">
            <div class="card-title">📁 Supported Formats</div>
            <div style="color: #B0BEC5; line-height: 2;">
                ✓ PDF Documents<br>
                ✓ Word (DOCX/DOC)<br>
                ✓ Text Files (TXT)<br>
                ✓ Images (JPG/PNG)<br>
                <span style="font-size: 0.85rem; color: #00A878;">🔒 Files are encrypted & secure</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    return uploaded_file


def render_risk_display(risk_result, settings):
    """Render the professional risk score display"""
    score = risk_result.overall_score
    level = risk_result.risk_level.value
    
    # Determine color class
    if score < 4:
        color_class = "risk-low"
        badge_class = "badge-low"
    elif score < 6:
        color_class = "risk-medium"
        badge_class = "badge-medium"
    elif score < 8:
        color_class = "risk-high"
        badge_class = "badge-high"
    else:
        color_class = "risk-critical"
        badge_class = "badge-critical"
    
    st.markdown(f"""
    <div class="risk-gauge">
        <div class="risk-score-big {color_class}">{score:.1f}</div>
        <div class="risk-label">out of 10</div>
        <div class="risk-badge {badge_class}">{level.upper()} RISK</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice announcement for accessibility
    if settings['accessibility_mode'] and settings['auto_read']:
        risk_message = f"Risk assessment complete. Overall risk score is {score:.1f} out of 10, rated as {level} risk."
        speak_text(risk_message, settings['voice_speed'])


def render_metrics_row(result, settings):
    """Render the metrics row"""
    cols = st.columns(4)
    
    metrics = [
        ("📋", result.total_clauses, "Total Clauses", "#D4AF37"),
        ("🚨", len(result.critical_clauses), "Critical Issues", "#DC3545"),
        ("📝", f"{result.word_count:,}", "Words", "#00A878"),
        ("📄", result.page_estimate, "Est. Pages", "#B0BEC5")
    ]
    
    for col, (icon, value, label, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 10px;">{icon}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_critical_clauses(critical_clauses, settings):
    """Render critical clauses section"""
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">🚨</span>
        Critical Clauses Requiring Attention
    </div>
    """, unsafe_allow_html=True)
    
    if settings['accessibility_mode'] and settings['voice_enabled']:
        if st.button("🎤 Read Critical Clauses"):
            for clause in critical_clauses[:3]:
                speak_text(
                    f"Critical clause {clause['clause_id']}: {clause['text'][:200]}",
                    settings['voice_speed']
                )
    
    if not critical_clauses:
        st.markdown("""
        <div class="info-box">
            <span style="font-size: 1.5rem;">✅</span>
            <span style="font-size: 1.1rem; font-weight: 600; color: #00A878; margin-left: 10px;">
                No Critical Clauses Found
            </span>
            <p style="color: #B0BEC5; margin-top: 10px;">
                This contract does not contain any clauses flagged as critical risk.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for clause in critical_clauses:
        risk_class = "clause-critical" if clause['risk_level'] == 'critical' else "clause-warning"
        st.markdown(f"""
        <div class="clause-card {risk_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-weight: 700; color: #FFFFFF;">Clause {clause['clause_id']}</span>
                <span style="background: rgba(220, 53, 69, 0.3); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; color: #DC3545; font-weight: 600;">
                    RISK: {clause['risk_score']}/10
                </span>
            </div>
            <p style="color: #E0E0E0; line-height: 1.6; margin: 0;">{clause['text']}</p>
            <div style="margin-top: 15px; display: flex; flex-wrap: wrap; gap: 8px;">
                {''.join([f'<span style="background: rgba(255, 193, 7, 0.2); padding: 4px 12px; border-radius: 15px; font-size: 0.75rem; color: #FFC107;">{factor}</span>' for factor in clause['factors']])}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_recommendations(recommendations, settings):
    """Render recommendations section"""
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">💡</span>
        Recommendations & Action Items
    </div>
    """, unsafe_allow_html=True)
    
    if settings['accessibility_mode'] and settings['voice_enabled']:
        if st.button("🎤 Read Recommendations"):
            for rec in recommendations[:5]:
                speak_text(rec, settings['voice_speed'])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="recommendation-item">
                <span style="font-weight: 700; color: #28A745; margin-right: 10px;">{i}.</span>
                <span style="color: #E0E0E0;">{rec}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No specific recommendations at this time.")


def render_summary(result, settings):
    """Render contract summary with accessibility"""
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📝</span>
        Contract Summary
    </div>
    """, unsafe_allow_html=True)
    
    # Voice controls for accessibility
    if settings['accessibility_mode']:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Read Executive Summary", use_container_width=True):
                speak_text(result.executive_summary, settings['voice_speed'])
        with col2:
            if st.button("🎤 Read Plain Summary", use_container_width=True):
                speak_text(result.plain_language_summary, settings['voice_speed'])
    
    # Executive Summary
    with st.expander("📊 Executive Summary", expanded=True):
        st.markdown(f"""
        <div class="pro-card">
            {result.executive_summary.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    
    # Plain Language Summary
    with st.expander("🗣️ Plain Language Summary (Business-Friendly)", expanded=True):
        summary_text = result.plain_language_summary
        
        # Translate if needed
        if settings['output_language'] != 'en':
            translation_service = TranslationService()
            summary_text = translation_service.get_summary_in_language(
                summary_text, settings['output_language']
            )
        
        st.markdown(f"""
        <div class="pro-card">
            {summary_text.replace(chr(10), '<br>').replace('###', '<h4>').replace('**', '')}
        </div>
        """, unsafe_allow_html=True)


def render_export_section(result, settings):
    """Render export options"""
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📤</span>
        Export & Download
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):
                pdf_gen = PDFGenerator()
                pdf_path = pdf_gen.generate_report(result)
                
                if pdf_path:
                    with open(pdf_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Download PDF",
                            f.read(),
                            file_name=f"legifyx_report_{result.contract_id}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    st.success("✅ PDF Ready!")
                    
                    if settings['accessibility_mode'] and settings['auto_read']:
                        speak_text("PDF report has been generated and is ready for download.", settings['voice_speed'])
    
    with col2:
        if st.button("📋 Export JSON Data", use_container_width=True):
            result_dict = {
                'contract_id': result.contract_id,
                'analysis_timestamp': result.analysis_timestamp,
                'contract_type': result.contract_type,
                'word_count': result.word_count,
                'risk_score': result.risk_result.overall_score if result.risk_result else 0,
                'risk_level': result.risk_result.risk_level.value if result.risk_result else 'unknown',
                'total_clauses': result.total_clauses,
                'critical_clauses': result.critical_clauses,
                'recommendations': result.recommendations,
                'executive_summary': result.executive_summary
            }
            
            st.download_button(
                "⬇️ Download JSON",
                json.dumps(result_dict, indent=2),
                file_name=f"legifyx_data_{result.contract_id}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col3:
        if st.button("🔊 Generate Audio Summary", use_container_width=True):
            with st.spinner("Generating audio..."):
                tts = TTSService()
                audio_path = tts.generate_summary_audio(
                    result.plain_language_summary,
                    result.contract_id,
                    settings['output_language']
                )
                
                if audio_path:
                    st.success(f"✅ Audio saved!")
                    if settings['accessibility_mode']:
                        speak_text("Audio summary has been generated.", settings['voice_speed'])


def main():
    """Main application entry point"""
    load_premium_css()
    init_session_state()
    render_premium_header()
    
    # Sidebar with accessibility options
    settings = render_accessibility_sidebar()
    
    # Welcome voice for accessibility mode
    if settings['accessibility_mode'] and settings['voice_enabled']:
        if 'welcome_spoken' not in st.session_state:
            speak_text(
                "Welcome to Legifyx, your AI-powered legal contract analysis assistant. "
                "Accessibility mode is enabled. Use the voice buttons to navigate and hear content.",
                settings['voice_speed']
            )
            st.session_state.welcome_spoken = True
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload & Analyze",
        "📊 Analysis Results", 
        "📚 Templates & Resources",
        "📜 History & Audit"
    ])
    
    with tab1:
        uploaded_file = render_upload_section(settings)
        
        if uploaded_file:
            st.session_state.uploaded_file_name = uploaded_file.name
            
            # File info display
            st.markdown(f"""
            <div class="pro-card">
                <div class="card-title">📁 Selected File</div>
                <div style="color: #FFFFFF; font-size: 1.1rem;">{uploaded_file.name}</div>
                <div style="color: #B0BEC5; margin-top: 5px;">Size: {uploaded_file.size / 1024:.1f} KB</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Analyze button
            if st.button("🔍 ANALYZE CONTRACT", use_container_width=True, type="primary"):
                if settings['accessibility_mode'] and settings['voice_enabled']:
                    speak_text("Starting contract analysis. Please wait.", settings['voice_speed'])
                
                with st.spinner("🔄 Analyzing contract... This may take a moment."):
                    progress_bar = st.progress(0)
                    
                    try:
                        # Parse document
                        progress_bar.progress(20)
                        parser = DocumentParser()
                        file_bytes = uploaded_file.read()
                        text, metadata = parser.parse_bytes(file_bytes, uploaded_file.name)
                        
                        if not text.strip():
                            st.error("❌ Could not extract text from the document.")
                            if settings['accessibility_mode']:
                                speak_text("Error: Could not extract text from the document.", settings['voice_speed'])
                        else:
                            progress_bar.progress(50)
                            st.session_state.contract_text = text
                            
                            # Analyze
                            analyzer = ContractAnalyzer()
                            result = analyzer.analyze(text)
                            
                            progress_bar.progress(80)
                            
                            st.session_state.analysis_result = result
                            st.session_state.analysis_history.append({
                                'id': result.contract_id,
                                'filename': uploaded_file.name,
                                'timestamp': result.analysis_timestamp,
                                'risk_score': result.risk_result.overall_score if result.risk_result else 0,
                                'risk_level': result.risk_result.risk_level.value if result.risk_result else 'unknown'
                            })
                            
                            # Audit logging
                            audit = AuditLogger()
                            file_hash = hashlib.sha256(file_bytes).hexdigest()
                            audit.log_upload(uploaded_file.name, file_hash)
                            audit.log_analysis(
                                result.contract_id,
                                result.contract_type,
                                result.risk_result.overall_score if result.risk_result else 0
                            )
                            
                            progress_bar.progress(100)
                            
                            st.success("✅ Analysis Complete! View results in the 'Analysis Results' tab.")
                            st.balloons()
                            
                            if settings['accessibility_mode'] and settings['auto_read']:
                                speak_text(
                                    f"Analysis complete. The contract has been identified as a {result.contract_type}. "
                                    f"Overall risk score is {result.risk_result.overall_score:.1f} out of 10, "
                                    f"rated as {result.risk_result.risk_level.value} risk. "
                                    f"Navigate to the Analysis Results tab for detailed findings.",
                                    settings['voice_speed']
                                )
                    
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        if settings['accessibility_mode']:
                            speak_text(f"Error during analysis: {str(e)}", settings['voice_speed'])
    
    with tab2:
        result = st.session_state.analysis_result
        
        if result:
            # Contract info and risk score
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div class="pro-card">
                    <div class="card-title">📄 Contract Type</div>
                    <div style="font-size: 1.3rem; color: #D4AF37; font-weight: 700;">{result.contract_type}</div>
                    <div style="color: #B0BEC5; margin-top: 10px; font-size: 0.9rem;">
                        ID: {result.contract_id}<br>
                        Language: {result.language.upper()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if result.risk_result:
                    render_risk_display(result.risk_result, settings)
            
            with col2:
                render_metrics_row(result, settings)
                
                # Entity summary
                if result.entities:
                    st.markdown("""
                    <div class="pro-card">
                        <div class="card-title">📋 Key Entities Extracted</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    entity_cols = st.columns(3)
                    with entity_cols[0]:
                        st.markdown("**👥 Parties**")
                        for party in result.entities.parties[:3]:
                            st.markdown(f"• {party.name}")
                    
                    with entity_cols[1]:
                        st.markdown("**🏛️ Jurisdiction**")
                        st.markdown(result.entities.jurisdiction or "_Not specified_")
                        st.markdown("**📅 Duration**")
                        st.markdown(result.entities.duration or "_Not specified_")
                    
                    with entity_cols[2]:
                        st.markdown("**💰 Financial Terms**")
                        for amount in result.entities.amounts[:3]:
                            st.markdown(f"• {amount.amount}")
            
            st.markdown("---")
            
            # Detailed analysis tabs
            detail_tabs = st.tabs([
                "🚨 Critical Issues",
                "💡 Recommendations",
                "📝 Summary",
                "📤 Export"
            ])
            
            with detail_tabs[0]:
                render_critical_clauses(result.critical_clauses, settings)
                
                if result.unfavorable_terms:
                    st.markdown("""
                    <div class="section-header">
                        <span class="section-icon">⚠️</span>
                        Unfavorable Terms Detected
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for term in result.unfavorable_terms:
                        st.markdown(f"""
                        <div class="clause-card clause-warning">
                            <div style="font-weight: 700; color: #FFC107; margin-bottom: 10px;">{term['issue']}</div>
                            <p style="color: #E0E0E0;">{term['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            with detail_tabs[1]:
                render_recommendations(result.recommendations, settings)
                
                if result.missing_clauses:
                    st.markdown("""
                    <div class="section-header">
                        <span class="section-icon">📝</span>
                        Missing Recommended Clauses
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for missing in result.missing_clauses:
                        st.markdown(f"""
                        <div class="warning-box">
                            <span style="color: #FFC107;">⚠️</span>
                            <span style="color: #FFFFFF; margin-left: 10px;">{missing}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            with detail_tabs[2]:
                render_summary(result, settings)
            
            with detail_tabs[3]:
                render_export_section(result, settings)
        
        else:
            st.markdown("""
            <div class="pro-card" style="text-align: center; padding: 60px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">📄</div>
                <div style="font-size: 1.3rem; color: #FFFFFF; font-weight: 600;">No Analysis Results Yet</div>
                <div style="color: #B0BEC5; margin-top: 10px;">
                    Upload a contract document in the "Upload & Analyze" tab to get started.
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📚</span>
            Standard Contract Templates
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="pro-card">
            <div class="card-title">🎯 Coming Soon: SME-Friendly Templates</div>
            <div style="color: #B0BEC5; line-height: 2;">
                We're preparing a library of balanced, SME-friendly contract templates:<br><br>
                ✓ Employment Agreements<br>
                ✓ Vendor/Supplier Contracts<br>
                ✓ Service Level Agreements<br>
                ✓ Non-Disclosure Agreements<br>
                ✓ Partnership Deeds<br>
                ✓ Lease Agreements<br><br>
                <span style="color: #00A878;">All templates are designed with fair terms that protect both parties.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📜</span>
            Analysis History & Audit Trail
        </div>
        """, unsafe_allow_html=True)
        
        history = st.session_state.get('analysis_history', [])
        
        if history:
            for item in reversed(history):
                risk_color = "#28A745" if item['risk_score'] < 4 else "#FFC107" if item['risk_score'] < 7 else "#DC3545"
                st.markdown(f"""
                <div class="pro-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #FFFFFF;">📄 {item['filename']}</div>
                            <div style="color: #B0BEC5; font-size: 0.85rem; margin-top: 5px;">
                                ID: {item['id']} • Analyzed: {item['timestamp'][:19]}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.5rem; font-weight: 700; color: {risk_color};">{item['risk_score']:.1f}</div>
                            <div style="font-size: 0.75rem; color: #B0BEC5; text-transform: uppercase;">{item['risk_level']} RISK</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="pro-card" style="text-align: center; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 15px;">📜</div>
                <div style="color: #FFFFFF; font-weight: 600;">No Analysis History</div>
                <div style="color: #B0BEC5; margin-top: 10px;">
                    Your contract analyses will appear here for reference.
                </div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
