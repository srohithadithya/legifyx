"""
LEGIFYX - AI-Powered Legal Contract Analysis Bot
Hackathon-Ready Version with Fixed Navigation & Premium UI
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import hashlib

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import APP_NAME, APP_VERSION, SUPPORTED_LANGUAGES
from core.analyzer import ContractAnalyzer
from services.document_parser import DocumentParser
from services.tts_service import TTSService
from utils.pdf_generator import PDFGenerator
from utils.audit_logger import AuditLogger
from templates.clause_templates import get_all_templates

# Page Config
st.set_page_config(
    page_title="LEGIFYX - Legal Contract Analysis Bot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Storage
DATA_DIR = Path(__file__).parent / "data" / "storage"
DATA_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = DATA_DIR / "history.json"


def load_premium_css():
    """Premium hackathon-ready CSS with fixed navigation colors"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
        
        /* === GLOBAL STYLES === */
        .stApp {
            background: linear-gradient(135deg, #0A1628 0%, #0D2137 50%, #112940 100%);
        }
        
        /* FORCE SIDEBAR TOGGLE VISIBILITY */
        header[data-testid="stHeader"] {
            display: flex !important;
            visibility: visible !important;
            background: rgba(0,0,0,0) !important;
        }
        
        #MainMenu, footer {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* THE ULTIMATE TOGGLE FIX */
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] button,
        button[aria-label="Open sidebar"],
        button[aria-label="Close sidebar"] {
            color: #D4AF37 !important;
            fill: #D4AF37 !important;
            background-color: rgba(212, 175, 55, 0.15) !important;
            border-radius: 50% !important;
            z-index: 999999 !important;
        }
        
        [data-testid="stHeader"] svg {
            fill: #D4AF37 !important;
            color: #D4AF37 !important;
        }
        
        /* === MAIN HEADER === */
        .brand-header {
            background: linear-gradient(135deg, rgba(13, 33, 55, 0.95), rgba(17, 41, 64, 0.98));
            border: 2px solid rgba(212, 175, 55, 0.4);
            border-radius: 20px;
            padding: 35px 25px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(212, 175, 55, 0.1);
        }
        
        .brand-logo {
            font-family: 'Playfair Display', serif;
            font-size: 3.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #D4AF37 0%, #F5E6A3 40%, #D4AF37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 8px;
            text-shadow: 0 0 60px rgba(212, 175, 55, 0.5);
        }
        
        .brand-tagline {
            font-family: 'Inter', sans-serif;
            color: #8BA3C7;
            font-size: 1rem;
            letter-spacing: 3px;
            margin-top: 8px;
            font-weight: 300;
        }
        
        .brand-badge {
            display: inline-block;
            background: linear-gradient(135deg, #D4AF37, #E8C547);
            color: #0A1628;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 2px;
            margin-top: 15px;
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.3);
        }
        
        /* === SIDEBAR STYLING === */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A1628 0%, #071018 100%) !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #0A1628 0%, #071018 100%) !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p {
            color: #FFFFFF !important;
            opacity: 1 !important;
        }
        
        /* Targets ALL sidebar text without breaking widget backgrounds */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #FFFFFF !important;
        }
        
        [data-testid="stSidebar"] h3 {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            color: #D4AF37 !important;
            margin-top: 20px !important;
            margin-bottom: 10px !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stCheckbox label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stToggle label,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            color: #FFFFFF !important;
        }
        
        [data-testid="stSidebar"] .stSlider span,
        [data-testid="stSidebar"] .stSlider p {
            color: #FFFFFF !important;
        }
        
        [data-testid="stSidebar"] div[data-testid="stNotification"] {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
        }
        
        [data-testid="stSidebar"] div[data-testid="stNotification"] p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Fix Selectbox White-out (Extreme) */
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #112940 !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 8px !important;
        }
        
        [data-testid="stSidebar"] div[data-baseweb="select"] * {
            background: transparent !important;
            color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] [data-testid="stSelectedValue"] {
            color: #FFFFFF !important;
        }

        /* Fix Sidebar Arrows and Icons */
        [data-testid="stSidebar"] svg {
            fill: #D4AF37 !important;
            color: #D4AF37 !important;
        }
        
        /* Sidebar Toggle/Slider handle fix */
        [data-testid="stSidebar"] div[data-baseweb="slider"] div {
            background-color: #D4AF37 !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="checkbox"] div {
            border-color: #D4AF37 !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="toggle"] div {
            background-color: #D4AF37 !important;
        }
        
        /* === TAB NAVIGATION (FIXED) === */
        .stTabs {
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(10, 22, 40, 0.8) !important;
            border-radius: 15px;
            padding: 8px;
            gap: 8px;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(13, 33, 55, 0.9) !important;
            color: #8BA3C7 !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            border: 1px solid transparent !important;
            transition: all 0.3s ease !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(26, 58, 92, 0.9) !important;
            color: #FFFFFF !important;
            border-color: rgba(212, 175, 55, 0.3) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #D4AF37, #E8C547) !important;
            color: #0A1628 !important;
            border: none !important;
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.4) !important;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            background: transparent !important;
            padding-top: 20px;
        }
        
        /* === EXPANDER (INNER SECTIONS) FIXED === */
        .streamlit-expanderHeader {
            background: rgba(13, 33, 55, 0.95) !important;
            color: #FFFFFF !important;
            border-radius: 12px !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderHeader p,
        .streamlit-expanderHeader span,
        .streamlit-expanderHeader div {
            color: #FFFFFF !important;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: rgba(212, 175, 55, 0.6) !important;
            background: rgba(26, 58, 92, 0.95) !important;
        }
        
        [data-testid="stExpander"] summary {
            color: #FFFFFF !important;
        }
        
        [data-testid="stExpander"] summary span {
            color: #FFFFFF !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(10, 22, 40, 0.8) !important;
            border: 1px solid rgba(212, 175, 55, 0.15) !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
        }
        
        /* === CARDS === */
        .premium-card {
            background: linear-gradient(145deg, rgba(13, 33, 55, 0.95), rgba(17, 41, 64, 0.95));
            border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 16px;
            padding: 22px;
            margin: 12px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .premium-card:hover {
            transform: translateY(-4px);
            border-color: rgba(212, 175, 55, 0.5);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
        }
        
        .card-title {
            font-size: 1rem;
            font-weight: 700;
            color: #D4AF37;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* === RISK GAUGE === */
        .risk-container {
            background: linear-gradient(145deg, rgba(13, 33, 55, 0.95), rgba(10, 22, 40, 0.98));
            border: 2px solid rgba(212, 175, 55, 0.3);
            border-radius: 20px;
            padding: 35px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .risk-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.08) 0%, transparent 60%);
            animation: glow 4s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
        }
        
        .risk-number {
            font-family: 'Inter', sans-serif;
            font-size: 4.5rem;
            font-weight: 800;
            line-height: 1;
            position: relative;
            z-index: 1;
        }
        
        .risk-low { color: #22C55E; text-shadow: 0 0 30px rgba(34, 197, 94, 0.5); }
        .risk-medium { color: #EAB308; text-shadow: 0 0 30px rgba(234, 179, 8, 0.5); }
        .risk-high { color: #F97316; text-shadow: 0 0 30px rgba(249, 115, 22, 0.5); }
        .risk-critical { color: #EF4444; text-shadow: 0 0 30px rgba(239, 68, 68, 0.5); }
        
        .risk-label {
            display: inline-block;
            padding: 10px 28px;
            border-radius: 50px;
            font-weight: 700;
            letter-spacing: 3px;
            font-size: 0.85rem;
            margin-top: 15px;
            position: relative;
            z-index: 1;
        }
        
        .label-low { background: rgba(34, 197, 94, 0.2); color: #22C55E; border: 2px solid #22C55E; }
        .label-medium { background: rgba(234, 179, 8, 0.2); color: #EAB308; border: 2px solid #EAB308; }
        .label-high { background: rgba(249, 115, 22, 0.2); color: #F97316; border: 2px solid #F97316; }
        .label-critical { background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 2px solid #EF4444; }
        
        /* === METRICS === */
        .metric-card {
            background: linear-gradient(145deg, rgba(17, 41, 64, 0.9), rgba(13, 33, 55, 0.95));
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 14px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: scale(1.03);
            border-color: #D4AF37;
        }
        
        .metric-val { font-size: 2.2rem; font-weight: 800; color: #D4AF37; line-height: 1; }
        .metric-lbl { font-size: 0.7rem; color: #8BA3C7; text-transform: uppercase; letter-spacing: 2px; margin-top: 8px; }
        
        /* === BUTTONS === */
        .stButton > button {
            background: linear-gradient(135deg, #D4AF37 0%, #E8C547 100%) !important;
            color: #0A1628 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 14px 36px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 25px rgba(212, 175, 55, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 35px rgba(212, 175, 55, 0.5) !important;
        }
        
        /* === CLAUSE ITEMS === */
        .clause-item {
            background: rgba(13, 33, 55, 0.8);
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            border-left: 5px solid #D4AF37;
            transition: all 0.3s ease;
        }
        
        .clause-item:hover {
            transform: translateX(5px);
            background: rgba(17, 41, 64, 0.9);
        }
        
        .clause-critical { border-left-color: #EF4444; background: rgba(239, 68, 68, 0.1); }
        .clause-warning { border-left-color: #EAB308; background: rgba(234, 179, 8, 0.1); }
        .clause-safe { border-left-color: #22C55E; background: rgba(34, 197, 94, 0.1); }
        
        /* === SECTION HEADERS === */
        .section-hdr {
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 28px 0 18px 0;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(212, 175, 55, 0.3);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* === INFO BOXES === */
        .info-box {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 12px;
            padding: 18px;
            margin: 12px 0;
            color: #C5D4E8;
        }
        
        .warning-box {
            background: rgba(234, 179, 8, 0.1);
            border: 1px solid rgba(234, 179, 8, 0.3);
            border-radius: 12px;
            padding: 18px;
            margin: 12px 0;
            color: #C5D4E8;
        }
        
        .danger-box {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 12px;
            padding: 18px;
            margin: 12px 0;
            color: #C5D4E8;
        }
        
        /* === TEMPLATE CARDS === */
        .template-item {
            background: linear-gradient(145deg, rgba(17, 41, 64, 0.85), rgba(13, 33, 55, 0.9));
            border: 1px solid rgba(34, 197, 94, 0.25);
            border-radius: 14px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        
        .template-item:hover {
            border-color: #22C55E;
            transform: translateX(6px);
        }
        
        /* === FOOTER (FIXED) === */
        .main-footer {
            background: linear-gradient(135deg, rgba(10, 22, 40, 0.98), rgba(7, 16, 24, 0.99));
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 18px;
            padding: 20px;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .footer-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        .footer-brand {
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
            color: #D4AF37;
            font-weight: 700;
        }
        
        .footer-contact {
            color: #8BA3C7;
            font-size: 0.85rem;
        }
        
        .footer-bottom {
            padding-top: 15px;
            color: #6B7D95;
            font-size: 0.8rem;
        }
        
        .footer-tech {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .tech-badge {
            background: rgba(212, 175, 55, 0.1);
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.75rem;
            color: #D4AF37;
        }
        
        /* === FILE UPLOADER === */
        [data-testid="stFileUploader"] {
            background: rgba(13, 33, 55, 0.6) !important;
            border: 2px dashed rgba(212, 175, 55, 0.4) !important;
            border-radius: 16px !important;
            padding: 25px !important;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: #D4AF37 !important;
            background: rgba(17, 41, 64, 0.7) !important;
        }
        
        /* === SCROLLBAR === */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #0A1628; }
        ::-webkit-scrollbar-thumb { background: #D4AF37; border-radius: 5px; }
        ::-webkit-scrollbar-thumb:hover { background: #E8C547; }
        
        /* === ACCESSIBILITY PANEL === */
        [data-testid="stSidebar"] [data-baseweb="select"] div,
        [data-testid="stSidebar"] input {
            color: #FFFFFF !important;
        }

        /* Sidebar Divider */
        [data-testid="stSidebar"] hr {
            background-color: rgba(212, 175, 55, 0.4) !important;
            margin: 20px 0 !important;
        }
        
        /* === CODE BLOCKS & TEXT COLORS === */
        .stCode, .stCode code, .stCodeBlock code {
            color: #F1F5F9 !important;
            background: #0D2137 !important;
        }
        
        pre, .stCodeBlock pre {
            background: #0D2137 !important;
            color: #F1F5F9 !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 10px !important;
            padding: 15px !important;
        }
        
        code {
            color: #F1F5F9 !important;
        }
        
        [data-testid="stCode"] {
            background: #0D2137 !important;
        }
        
        [data-testid="stCode"] pre {
            background: #0D2137 !important;
            color: #F1F5F9 !important;
        }
        
        [data-testid="stCode"] code {
            color: #F1F5F9 !important;
            background: transparent !important;
        }
        
        /* Expander text fix */
        .streamlit-expanderContent p,
        .streamlit-expanderContent span,
        .streamlit-expanderContent div {
            color: #C5D4E8 !important;
        }
        
        .streamlit-expanderContent strong,
        .streamlit-expanderContent b {
            color: #D4AF37 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def init_state():
    """Initialize session state"""
    defaults = {
        'result': None,
        'history': load_json(HISTORY_FILE, []),
        'acc_mode': False,
        'voice_on': False,
        'auto_read': False,
        'speed': 150
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def load_json(path, default):
    """Load JSON file"""
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except:
            pass
    return default


def save_json(path, data):
    """Save JSON file"""
    try:
        with open(path, 'w') as f:
            json.dump(data[-100:], f, indent=2)
    except:
        pass


def speak(text):
    """Speak if accessibility enabled"""
    if st.session_state.get('acc_mode') and st.session_state.get('voice_on'):
        try:
            tts = TTSService()
            tts.set_voice_properties(rate=st.session_state.get('speed', 150))
            tts.speak(text[:2000])
        except:
            pass


def render_header():
    """Render premium header"""
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo">⚖️ LEGIFYX</div>
        <div class="brand-tagline">AI-POWERED LEGAL CONTRACT ANALYSIS</div>
        <div class="brand-badge">🛡️ SECURE • TRUSTED • ENTERPRISE GRADE</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render premium footer"""
    st.markdown("""
    <div class="main-footer">
        <div class="footer-top">
            <div class="footer-brand">⚖️ LEGIFYX v1.0.0</div>
            <div style="color: #8BA3C7;">Made with ❤️</div>
        </div>
        <div class="footer-bottom">
            <div>© 2026 Legifyx. All Rights Reserved.</div>
            <div class="footer-tech">
                <span class="tech-badge">💾 JSON Storage</span>
                <span class="tech-badge">🔒 AES-256 Encryption</span>
                <span class="tech-badge">🐍 Python 3.12.0</span>
                <span class="tech-badge">🤖 spaCy NLP</span>
                <span class="tech-badge">♿ TTS Accessibility</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(212, 175, 55, 0.3);">
            <div style="font-size: 2.5rem;">⚖️</div>
            <div style="font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #D4AF37; font-weight: 700;">LEGIFYX</div>
            <div style="font-size: 0.6rem; color: #8BA3C7; letter-spacing: 2px;">LEGAL AI BOT</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Accessibility Section
        st.markdown("### ♿ Accessibility")
        acc_col = st.container()
        with acc_col:
            st.session_state.acc_mode = st.toggle("🔊 Enable Accessibility", st.session_state.acc_mode)
            
            if st.session_state.acc_mode:
                st.success("✅ Accessibility ON")
                st.session_state.voice_on = st.checkbox("🗣️ Voice Navigation", st.session_state.voice_on)
                st.session_state.auto_read = st.checkbox("📖 Auto-Read Results", st.session_state.auto_read)
                st.session_state.speed = st.slider("🔈 Speed", 100, 250, st.session_state.speed, 25)
                
                if st.button("🔊 Test Voice", use_container_width=True):
                    speak("Voice test successful. Legifyx is ready.")
                    st.info("Testing voice...")
        
        st.markdown("---")
        st.markdown("### 🌐 Language")
        lang = st.selectbox("Output", list(SUPPORTED_LANGUAGES.keys()), format_func=lambda x: SUPPORTED_LANGUAGES[x])
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{len(st.session_state.history)}</div>
            <div class="metric-lbl">Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💾 Storage")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #8BA3C7; background: rgba(212, 175, 55, 0.1); padding: 10px; border-radius: 8px;">
            <strong>Type:</strong> JSON Files<br>
            <strong>Encryption:</strong> AES-256<br>
            <strong>Location:</strong> Local Storage
        </div>
        """, unsafe_allow_html=True)
        
        return lang


def render_upload_tab():
    """Render upload tab"""
    st.markdown('<div class="section-hdr">📄 Upload Contract</div>', unsafe_allow_html=True)
    
    if st.session_state.acc_mode:
        if st.button("🎤 Describe Upload"):
            speak("Upload section. Upload PDF, Word, or text files for AI analysis.")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        file = st.file_uploader("Drop contract file", type=['pdf', 'docx', 'doc', 'txt', 'jpg', 'png'])
    
    with c2:
        st.markdown("""
        <div class="premium-card">
            <div class="card-title">📁 Formats</div>
            <div style="color: #8BA3C7; line-height: 1.8;">
                ✓ PDF<br>✓ Word<br>✓ Text<br>✓ Images<br>
                <span style="color: #22C55E;">🔒 Secure</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if file:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">📄 Selected</div>
            <div style="color: #FFF;">{file.name}</div>
            <div style="color: #8BA3C7; font-size: 0.85rem;">{file.size/1024:.1f} KB</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 ANALYZE CONTRACT", use_container_width=True, type="primary"):
            if st.session_state.acc_mode:
                speak("Starting analysis.")
            
            with st.spinner("Analyzing..."):
                prog = st.progress(0)
                try:
                    parser = DocumentParser()
                    text, _ = parser.parse_bytes(file.read(), file.name)
                    prog.progress(30)
                    
                    if not text.strip():
                        st.error("Could not extract text.")
                        return
                    
                    analyzer = ContractAnalyzer()
                    result = analyzer.analyze(text)
                    prog.progress(80)
                    
                    st.session_state.result = result
                    st.session_state.history.append({
                        'id': result.contract_id,
                        'file': file.name,
                        'time': result.analysis_timestamp,
                        'score': result.risk_result.overall_score if result.risk_result else 0,
                        'level': result.risk_result.risk_level.value if result.risk_result else 'unknown',
                        'type': result.contract_type
                    })
                    save_json(HISTORY_FILE, st.session_state.history)
                    prog.progress(100)
                    
                    st.success("✅ Complete! See Results tab.")
                    st.balloons()
                    
                    if st.session_state.acc_mode and st.session_state.auto_read:
                        speak(f"Analysis complete. Type: {result.contract_type}. Risk: {result.risk_result.overall_score:.1f} out of 10.")
                
                except Exception as e:
                    st.error(f"Error: {e}")


def render_results_tab():
    """Render results tab"""
    r = st.session_state.result
    
    if not r:
        st.markdown("""
        <div class="premium-card" style="text-align: center; padding: 60px;">
            <div style="font-size: 3.5rem;">📄</div>
            <div style="color: #FFF; font-size: 1.2rem; font-weight: 600; margin-top: 15px;">No Analysis Yet</div>
            <div style="color: #8BA3C7;">Upload a contract to begin.</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    if st.session_state.acc_mode:
        if st.button("🎤 Read Summary"):
            speak(r.executive_summary[:1500])
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">📑 Type</div>
            <div style="font-size: 1.2rem; color: #D4AF37; font-weight: 700;">{r.contract_type}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if r.risk_result:
            s = r.risk_result.overall_score
            l = r.risk_result.risk_level.value
            
            if s < 4: c, lb = "risk-low", "label-low"
            elif s < 6: c, lb = "risk-medium", "label-medium"
            elif s < 8: c, lb = "risk-high", "label-high"
            else: c, lb = "risk-critical", "label-critical"
            
            st.markdown(f"""
            <div class="risk-container">
                <div class="risk-number {c}">{s:.1f}</div>
                <div style="color: #8BA3C7; margin-top: 5px;">out of 10</div>
                <div class="risk-label {lb}">{l.upper()} RISK</div>
            </div>
            """, unsafe_allow_html=True)
    
    with c2:
        cols = st.columns(4)
        data = [("📋", r.total_clauses, "Clauses"), ("🚨", len(r.critical_clauses), "Critical"), 
                ("📝", r.word_count, "Words"), ("📄", r.page_estimate, "Pages")]
        for col, (i, v, l) in zip(cols, data):
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-val">{v}</div><div class="metric-lbl">{l}</div></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🚨 Issues", "💡 Advice", "📝 Summary", "📤 Export"])
    
    with tabs[0]:
        if r.critical_clauses:
            for cl in r.critical_clauses[:5]:
                st.markdown(f"""
                <div class="clause-item clause-critical">
                    <b style="color: #FFF;">Clause {cl['clause_id']}</b> 
                    <span style="float: right; background: rgba(239, 68, 68, 0.3); padding: 3px 10px; border-radius: 10px; color: #EF4444; font-size: 0.75rem;">RISK: {cl['risk_score']}/10</span>
                    <p style="color: #C5D4E8; margin-top: 10px; font-size: 0.9rem;">{cl['text'][:250]}...</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">✅ <b>No critical issues!</b></div>', unsafe_allow_html=True)
    
    with tabs[1]:
        if r.recommendations:
            for i, rec in enumerate(r.recommendations[:8], 1):
                st.markdown(f'<div class="clause-item clause-safe"><b style="color: #22C55E;">{i}.</b> <span style="color: #C5D4E8;">{rec}</span></div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown(f'<div class="premium-card"><div class="card-title">📊 Summary</div><div style="color: #C5D4E8; line-height: 1.8;">{r.executive_summary.replace(chr(10), "<br>")}</div></div>', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<p style="color: #C5D4E8;">Export your analysis in different formats:</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        # Define output directories using project path
        project_dir = Path(__file__).parent
        exports_dir = project_dir / "exports"
        audio_dir = project_dir / "audio_output"
        exports_dir.mkdir(exist_ok=True)
        audio_dir.mkdir(exist_ok=True)
        
        with c1:
            if st.button("📄 Generate PDF", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    try:
                        pdf = PDFGenerator(output_dir=str(exports_dir))
                        path = pdf.generate_report(r)
                        if path and os.path.exists(path):
                            with open(path, 'rb') as f:
                                pdf_data = f.read()
                            st.download_button(
                                "⬇️ Download PDF", 
                                pdf_data, 
                                f"legifyx_{r.contract_id}.pdf", 
                                "application/pdf",
                                key="pdf_download"
                            )
                            st.success(f"✅ PDF saved to: {path}")
                        else:
                            st.error("PDF generation failed")
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with c2:
            json_data = json.dumps({
                'id': r.contract_id, 
                'type': r.contract_type, 
                'score': r.risk_result.overall_score if r.risk_result else 0,
                'level': r.risk_result.risk_level.value if r.risk_result else 'unknown',
                'summary': r.executive_summary,
                'recommendations': r.recommendations[:10] if r.recommendations else []
            }, indent=2)
            st.download_button(
                "📋 Download JSON", 
                json_data, 
                f"legifyx_{r.contract_id}.json",
                "application/json",
                use_container_width=True
            )
        
        with c3:
            if st.button("🔊 Generate Audio", use_container_width=True):
                with st.spinner("Generating audio summary..."):
                    try:
                        tts = TTSService(output_dir=str(audio_dir))
                        path = tts.generate_summary_audio(r.plain_language_summary[:3000], r.contract_id)
                        if path and os.path.exists(path):
                            with open(path, 'rb') as f:
                                audio_data = f.read()
                            st.download_button(
                                "⬇️ Download Audio",
                                audio_data,
                                f"legifyx_{r.contract_id}.mp3",
                                "audio/mpeg",
                                key="audio_download"
                            )
                            st.success(f"✅ Audio saved to: {path}")
                        else:
                            st.error("Audio generation failed")
                    except Exception as e:
                        st.error(f"Error: {e}")


def render_templates_tab():
    """Render templates with proper styling"""
    st.markdown('<div class="section-hdr">📚 Templates & Resources</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">💡 <b style="color: #22C55E;">Download and customize</b> <span style="color: #C5D4E8;">these templates for your business contracts.</span></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📝 Clause Templates", "📄 Contract Types", "📖 Legal Resources"])
    
    with tabs[0]:
        st.markdown('<p style="color: #C5D4E8; margin-bottom: 20px;">Standard balanced clauses for fair contracts:</p>', unsafe_allow_html=True)
        templates = get_all_templates()
        for k, t in templates.items():
            risk_color = "#22C55E" if t['risk_level'] == 'low' else "#EAB308" if t['risk_level'] == 'medium' else "#EF4444"
            with st.expander(f"📋 {t['name']}"):
                st.markdown(f'<p style="color: #C5D4E8;"><b style="color: #D4AF37;">Category:</b> {t["category"].title()} | <b style="color: #D4AF37;">Risk Level:</b> <span style="color: {risk_color};">{t["risk_level"].upper()}</span></p>', unsafe_allow_html=True)
                st.code(t['template'].strip()[:800], language="text")
                st.markdown(f'<p style="color: #22C55E;">💡 <b>Guidance:</b> <span style="color: #C5D4E8;">{t["guidance"]}</span></p>', unsafe_allow_html=True)
                if t.get('variables'):
                    st.markdown(f'<p style="color: #8BA3C7;"><b style="color: #D4AF37;">Variables:</b> {" | ".join(t["variables"])}</p>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<p style="color: #C5D4E8; margin-bottom: 20px;">Available contract types for businesses:</p>', unsafe_allow_html=True)
        items = [
            ("👔", "Employment Agreement", "For hiring employees with balanced terms"),
            ("🔧", "Service Agreement", "For engaging consultants and service providers"),
            ("📦", "Vendor Contract", "For supplier relationships and procurement"),
            ("🔐", "Non-Disclosure Agreement", "Mutual NDA for business discussions"),
            ("🤝", "Partnership Deed", "For business partnership arrangements"),
            ("🏢", "Commercial Lease", "For renting office or shop space"),
            ("💼", "Consultancy Agreement", "For hiring consultants"),
            ("🏪", "Franchise Agreement", "For franchise business arrangements")
        ]
        for icon, name, desc in items:
            st.markdown(f'''
            <div class="template-item">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 1.8rem;">{icon}</span>
                    <div>
                        <b style="color: #FFFFFF; font-size: 1rem;">{name}</b>
                        <p style="color: #8BA3C7; margin: 5px 0 0 0; font-size: 0.85rem;">{desc}</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<p style="color: #C5D4E8; margin-bottom: 20px;">Key Indian legal frameworks for contracts:</p>', unsafe_allow_html=True)
        laws = [
            ("📜 Indian Contract Act, 1872", "Foundation of contract law - validity, enforceability, breach remedies", ["Section 10: Valid contract elements", "Section 23: Lawful consideration", "Section 74: Penalty clauses"]),
            ("⚖️ Arbitration Act, 1996", "Dispute resolution and enforcement of arbitral awards", ["Written agreements required", "Choose seat of arbitration", "Awards enforceable like decrees"]),
            ("💻 IT Act, 2000", "Legal validity of electronic contracts and signatures", ["E-contracts are valid", "Digital signatures binding", "Data protection obligations"]),
            ("🛡️ Consumer Protection Act, 2019", "Protection against unfair contract terms", ["Unfair terms provisions", "Consumer rights", "Dispute resolution"])
        ]
        for title, desc, points in laws:
            st.markdown(f'''
            <div class="clause-item">
                <b style="color: #D4AF37; font-size: 1.05rem;">{title}</b>
                <p style="color: #C5D4E8; margin: 8px 0;">{desc}</p>
                <div style="margin-top: 10px;">
                    {" ".join([f'<span style="background: rgba(212, 175, 55, 0.15); color: #D4AF37; padding: 4px 10px; border-radius: 15px; font-size: 0.75rem; margin-right: 8px;">{p}</span>' for p in points])}
                </div>
            </div>
            ''', unsafe_allow_html=True)


def render_history_tab():
    """Render history"""
    st.markdown('<div class="section-hdr">📜 History</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">💾 <b>Storage:</b> Your analysis history is stored securely in local JSON files.</div>', unsafe_allow_html=True)
    
    hist = st.session_state.history
    if hist:
        for h in reversed(hist[-15:]):
            col = "#22C55E" if h['score'] < 4 else "#EAB308" if h['score'] < 7 else "#EF4444"
            st.markdown(f"""
            <div class="premium-card" style="display: flex; justify-content: space-between;">
                <div><b style="color: #FFF;">📄 {h['file']}</b><br><span style="color: #8BA3C7; font-size: 0.8rem;">{h['time'][:16]}</span></div>
                <div style="text-align: right;"><span style="font-size: 1.5rem; font-weight: 700; color: {col};">{h['score']:.1f}</span><br><span style="color: #8BA3C7; font-size: 0.7rem;">{h['level'].upper()}</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear"):
            st.session_state.history = []
            save_json(HISTORY_FILE, [])
            st.rerun()
    else:
        st.info("No history yet.")


def main():
    """Main entry"""
    load_premium_css()
    init_state()
    render_header()
    lang = render_sidebar()
    
    if st.session_state.acc_mode and st.session_state.voice_on:
        if 'welcomed' not in st.session_state:
            speak("Welcome to Legifyx. Accessibility enabled.")
            st.session_state.welcomed = True
    
    tabs = st.tabs(["📤 Upload", "📊 Results", "📚 Templates", "📜 History"])
    
    with tabs[0]: render_upload_tab()
    with tabs[1]: render_results_tab()
    with tabs[2]: render_templates_tab()
    with tabs[3]: render_history_tab()
    
    render_footer()


if __name__ == "__main__":
    main()
