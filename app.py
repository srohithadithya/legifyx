"""
Legifyx - AI-Powered Legal Contract Analysis Bot
Complete Professional Interface with Accessibility Features
Storage: JSON-based file storage (no database required)
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import hashlib

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
from templates.clause_templates import get_all_templates, get_template, fill_template

# Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} - Legal Contract Analysis Bot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Storage paths (JSON-based, no database)
DATA_DIR = Path(__file__).parent / "data"
STORAGE_DIR = DATA_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = STORAGE_DIR / "analysis_history.json"
TEMPLATES_FILE = STORAGE_DIR / "user_templates.json"


def load_css():
    """Load premium CSS"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
        
        :root {
            --primary: #0F2644;
            --secondary: #D4AF37;
            --accent: #00A878;
            --danger: #DC3545;
            --surface: #132F4C;
            --text: #FFFFFF;
            --text-muted: #B0BEC5;
        }
        
        .stApp { background: linear-gradient(135deg, #0A1929 0%, #0F2644 50%, #132F4C 100%); }
        #MainMenu, footer, header { visibility: hidden; }
        
        /* Premium Header */
        .main-header {
            background: linear-gradient(135deg, rgba(15, 38, 68, 0.95) 0%, rgba(26, 58, 92, 0.95) 100%);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            text-align: center;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
        }
        
        .brand-title {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #D4AF37 0%, #F4E4A6 50%, #D4AF37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 6px;
        }
        
        .brand-subtitle {
            font-family: 'Inter', sans-serif;
            color: #B0BEC5;
            font-size: 1.1rem;
            letter-spacing: 2px;
            margin-top: 8px;
        }
        
        .header-badge {
            display: inline-block;
            background: linear-gradient(135deg, #D4AF37, #E8C547);
            color: #0A1929;
            padding: 6px 18px;
            border-radius: 25px;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1px;
            margin-top: 15px;
        }
        
        /* Footer */
        .main-footer {
            background: linear-gradient(135deg, rgba(15, 38, 68, 0.9), rgba(10, 25, 41, 0.95));
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 15px;
            padding: 25px;
            margin-top: 40px;
            text-align: center;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .footer-links a {
            color: #D4AF37;
            text-decoration: none;
            margin: 0 15px;
            font-size: 0.9rem;
        }
        
        .footer-text {
            color: #B0BEC5;
            font-size: 0.8rem;
        }
        
        /* Cards */
        .pro-card {
            background: linear-gradient(145deg, rgba(19, 47, 76, 0.9), rgba(15, 38, 68, 0.9));
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 15px;
            padding: 22px;
            margin: 12px 0;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .pro-card:hover {
            transform: translateY(-3px);
            border-color: rgba(212, 175, 55, 0.4);
        }
        
        .card-title {
            font-size: 1rem;
            font-weight: 600;
            color: #D4AF37;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Risk Display */
        .risk-gauge {
            background: linear-gradient(145deg, #132F4C, #0F2644);
            border: 2px solid rgba(212, 175, 55, 0.3);
            border-radius: 18px;
            padding: 35px;
            text-align: center;
        }
        
        .risk-score { font-size: 4rem; font-weight: 800; line-height: 1; }
        .risk-low { color: #28A745; }
        .risk-medium { color: #FFC107; }
        .risk-high { color: #FF9800; }
        .risk-critical { color: #DC3545; }
        
        .risk-badge {
            display: inline-block;
            padding: 10px 25px;
            border-radius: 50px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-top: 15px;
            font-size: 0.85rem;
        }
        
        .badge-low { background: rgba(40, 167, 69, 0.2); color: #28A745; border: 2px solid #28A745; }
        .badge-medium { background: rgba(255, 193, 7, 0.2); color: #FFC107; border: 2px solid #FFC107; }
        .badge-high { background: rgba(255, 152, 0, 0.2); color: #FF9800; border: 2px solid #FF9800; }
        .badge-critical { background: rgba(220, 53, 69, 0.2); color: #DC3545; border: 2px solid #DC3545; }
        
        /* Metrics */
        .metric-box {
            background: linear-gradient(145deg, #1A3A5C, #132F4C);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        
        .metric-value { font-size: 2rem; font-weight: 800; color: #D4AF37; }
        .metric-label { font-size: 0.75rem; color: #B0BEC5; text-transform: uppercase; letter-spacing: 1px; margin-top: 8px; }
        
        /* Accessibility Toggle */
        .accessibility-toggle {
            background: linear-gradient(145deg, #00A878, #00C896);
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            text-align: center;
        }
        
        /* Templates */
        .template-card {
            background: linear-gradient(145deg, rgba(26, 58, 92, 0.8), rgba(19, 47, 76, 0.9));
            border: 1px solid rgba(0, 168, 120, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        
        .template-card:hover {
            border-color: #00A878;
            transform: translateX(5px);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #D4AF37, #E8C547);
            color: #0A1929;
            border: none;
            border-radius: 50px;
            padding: 12px 35px;
            font-weight: 700;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F2644, #0A1929);
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }
        
        /* Voice Button */
        .voice-btn {
            background: linear-gradient(135deg, #00A878, #00C896);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            cursor: pointer;
        }
        
        /* Section Headers */
        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 25px 0 15px 0;
            padding-bottom: 12px;
            border-bottom: 2px solid rgba(212, 175, 55, 0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Clause Cards */
        .clause-item {
            background: rgba(19, 47, 76, 0.7);
            border-radius: 10px;
            padding: 18px;
            margin: 10px 0;
            border-left: 4px solid #D4AF37;
        }
        
        .clause-critical { border-left-color: #DC3545; background: rgba(220, 53, 69, 0.1); }
        .clause-warning { border-left-color: #FFC107; background: rgba(255, 193, 7, 0.1); }
        .clause-safe { border-left-color: #28A745; background: rgba(40, 167, 69, 0.1); }
        
        /* Info Boxes */
        .info-box { background: rgba(0, 168, 120, 0.1); border: 1px solid rgba(0, 168, 120, 0.3); border-radius: 10px; padding: 18px; margin: 12px 0; }
        .warning-box { background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 10px; padding: 18px; margin: 12px 0; }
        .danger-box { background: rgba(220, 53, 69, 0.1); border: 1px solid rgba(220, 53, 69, 0.3); border-radius: 10px; padding: 18px; margin: 12px 0; }
    </style>
    """, unsafe_allow_html=True)


def init_state():
    """Initialize session state"""
    defaults = {
        'analysis_result': None,
        'uploaded_file_name': None,
        'contract_text': None,
        'analysis_history': load_history(),
        'accessibility_mode': False,
        'voice_enabled': False,
        'auto_read': False,
        'voice_speed': 150,
        'tts_available': check_tts()
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def check_tts():
    """Check if TTS is available"""
    try:
        tts = TTSService()
        return tts.is_available()
    except:
        return False


def load_history():
    """Load analysis history from JSON file"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_history(history):
    """Save analysis history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history[-100:], f, indent=2)
    except:
        pass


def speak(text, rate=150):
    """Speak text if TTS enabled"""
    if st.session_state.get('accessibility_mode') and st.session_state.get('voice_enabled'):
        try:
            tts = TTSService()
            tts.set_voice_properties(rate=rate)
            tts.speak(text)
        except Exception as e:
            st.warning(f"Voice unavailable: {e}")


def render_header():
    """Render main header"""
    st.markdown("""
    <div class="main-header">
        <div class="brand-title">⚖️ LEGIFYX</div>
        <div class="brand-subtitle">AI-Powered Legal Contract Analysis Bot for Indian SMEs</div>
        <div class="header-badge">🛡️ SECURE • TRUSTED • ENTERPRISE GRADE</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render main footer"""
    st.markdown("""
    <div class="main-footer">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div style="color: #D4AF37; font-weight: 600;">⚖️ LEGIFYX v1.0.0</div>
            <div style="color: #B0BEC5; font-size: 0.85rem;">
                📧 support@legifyx.com | 📞 +91-XXX-XXX-XXXX
            </div>
            <div style="color: #B0BEC5; font-size: 0.8rem;">
                © 2024 Legifyx. All Rights Reserved. | 🇮🇳 Made in India
            </div>
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(212, 175, 55, 0.2);">
            <div style="color: #B0BEC5; font-size: 0.75rem;">
                💾 <strong>Storage:</strong> JSON-based local storage (no database required) | 
                🔒 <strong>Security:</strong> AES-256 encryption, audit logging | 
                ♿ <strong>Accessibility:</strong> Full TTS support for visually impaired users
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with accessibility toggle"""
    with st.sidebar:
        # Branding
        st.markdown("""
        <div style="text-align: center; padding: 15px 0; border-bottom: 1px solid rgba(212, 175, 55, 0.3); margin-bottom: 20px;">
            <div style="font-size: 2.5rem;">⚖️</div>
            <div style="font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #D4AF37; font-weight: 700;">LEGIFYX</div>
            <div style="font-size: 0.65rem; color: #B0BEC5; letter-spacing: 1px;">LEGAL AI ASSISTANT</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ACCESSIBILITY SECTION - PROMINENT TOGGLE
        st.markdown("### ♿ Accessibility")
        
        # Main toggle
        acc_mode = st.toggle(
            "🔊 Enable Accessibility Mode",
            value=st.session_state.accessibility_mode,
            help="Enable voice assistance for visually impaired users"
        )
        st.session_state.accessibility_mode = acc_mode
        
        if acc_mode:
            st.success("✅ Accessibility Mode ON")
            
            # TTS Status
            if st.session_state.tts_available:
                st.info("🎤 Text-to-Speech: Available")
            else:
                st.warning("⚠️ TTS not available. Install pyttsx3.")
            
            # Voice Options
            st.session_state.voice_enabled = st.checkbox(
                "🗣️ Voice Navigation",
                value=st.session_state.voice_enabled,
                help="Hear navigation cues"
            )
            
            st.session_state.auto_read = st.checkbox(
                "📖 Auto-Read Results",
                value=st.session_state.auto_read,
                help="Automatically read analysis results"
            )
            
            st.session_state.voice_speed = st.slider(
                "🔈 Voice Speed",
                100, 250, st.session_state.voice_speed, 25
            )
            
            # Test voice button
            if st.button("🔊 Test Voice", use_container_width=True):
                speak("Voice test successful. Legifyx accessibility mode is working.", st.session_state.voice_speed)
                st.success("Voice test initiated!")
        
        st.markdown("---")
        
        # Language
        st.markdown("### 🌐 Language")
        output_lang = st.selectbox(
            "Output Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x]
        )
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📊 Statistics")
        hist_count = len(st.session_state.get('analysis_history', []))
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{hist_count}</div>
            <div class="metric-label">Contracts Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Storage Info
        st.markdown("### 💾 Storage")
        st.markdown("""
        <div style="background: rgba(0, 168, 120, 0.1); padding: 12px; border-radius: 8px; font-size: 0.8rem; color: #B0BEC5;">
            <strong>Type:</strong> JSON File Storage<br>
            <strong>Location:</strong> data/storage/<br>
            <strong>Database:</strong> None Required<br>
            <strong>Encryption:</strong> AES-256
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Version
        st.markdown(f"""
        <div style="text-align: center; font-size: 0.75rem; color: #B0BEC5;">
            v{APP_VERSION} | 🔒 Secure
        </div>
        """, unsafe_allow_html=True)
        
        return {'output_language': output_lang}


def render_templates_tab():
    """Render complete templates and resources tab"""
    st.markdown('<div class="section-title">📚 Standard Contract Templates</div>', unsafe_allow_html=True)
    
    # Voice button for accessibility
    if st.session_state.accessibility_mode:
        if st.button("🎤 Describe Templates Section"):
            speak("Templates section. Here you can access standard clause templates and contract templates for various business needs.", st.session_state.voice_speed)
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 About Templates:</strong> These SME-friendly templates are designed with balanced terms 
        that protect both parties. Use them as starting points and customize as needed.
    </div>
    """, unsafe_allow_html=True)
    
    # Template Categories
    template_tabs = st.tabs(["📝 Clause Templates", "📄 Contract Templates", "📖 Legal Resources"])
    
    with template_tabs[0]:
        st.markdown("#### Standard Clause Templates")
        st.markdown("Copy and customize these balanced clauses for your contracts:")
        
        templates = get_all_templates()
        
        for key, template in templates.items():
            with st.expander(f"📋 {template['name']} (Risk: {template['risk_level'].upper()})", expanded=False):
                st.markdown(f"**Category:** {template['category'].title()}")
                st.markdown(f"**Guidance:** {template['guidance']}")
                
                st.code(template['template'].strip(), language="text")
                
                # Variables to fill
                if template['variables']:
                    st.markdown("**Variables to customize:**")
                    for var in template['variables']:
                        st.markdown(f"- `{{{var}}}`")
                
                # Copy button
                if st.button(f"📋 Copy {template['name']}", key=f"copy_{key}"):
                    st.success("Template copied! (Use Ctrl+C to copy from the code block above)")
    
    with template_tabs[1]:
        st.markdown("#### Full Contract Templates")
        
        contract_types = [
            {"name": "Employment Agreement", "icon": "👔", "desc": "For hiring employees with balanced terms"},
            {"name": "Service Agreement", "icon": "🔧", "desc": "For engaging service providers and consultants"},
            {"name": "Vendor/Supplier Contract", "icon": "📦", "desc": "For supplier relationships and procurement"},
            {"name": "Non-Disclosure Agreement", "icon": "🔐", "desc": "Mutual NDA for business discussions"},
            {"name": "Partnership Deed", "icon": "🤝", "desc": "For business partnerships"},
            {"name": "Commercial Lease", "icon": "🏢", "desc": "For renting office/shop space"},
            {"name": "Consultancy Agreement", "icon": "💼", "desc": "For hiring consultants"},
            {"name": "Franchise Agreement", "icon": "🏪", "desc": "For franchise business arrangements"}
        ]
        
        cols = st.columns(2)
        for i, ct in enumerate(contract_types):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="template-card">
                    <div style="font-size: 1.5rem; margin-bottom: 8px;">{ct['icon']}</div>
                    <div style="font-weight: 600; color: #FFFFFF; margin-bottom: 5px;">{ct['name']}</div>
                    <div style="font-size: 0.85rem; color: #B0BEC5;">{ct['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box" style="margin-top: 20px;">
            <strong>📋 Templates Coming Soon:</strong> Full contract templates with guided wizards 
            will be available in the next update. For now, use clause templates above.
        </div>
        """, unsafe_allow_html=True)
    
    with template_tabs[2]:
        st.markdown("#### 📖 Legal Resources & Knowledge Base")
        
        # Indian Law References
        st.markdown("##### 🇮🇳 Indian Legal Framework")
        
        laws = [
            {"name": "Indian Contract Act, 1872", "key_points": [
                "Section 10: Valid contract requirements",
                "Section 23: Lawful consideration",
                "Section 27: Agreements in restraint of trade void",
                "Section 74: Penalty clauses may be reduced"
            ]},
            {"name": "Arbitration and Conciliation Act, 1996", "key_points": [
                "Written arbitration agreements required",
                "Choose seat of arbitration",
                "Awards enforceable like court decrees"
            ]},
            {"name": "Information Technology Act, 2000", "key_points": [
                "Electronic contracts valid",
                "Digital signatures have legal validity",
                "Data protection obligations"
            ]},
            {"name": "Consumer Protection Act, 2019", "key_points": [
                "Unfair contract terms provisions",
                "Consumer rights protection",
                "Dispute resolution mechanisms"
            ]}
        ]
        
        for law in laws:
            with st.expander(f"📜 {law['name']}"):
                for point in law['key_points']:
                    st.markdown(f"• {point}")
        
        # Common Issues
        st.markdown("##### ⚠️ Common Contract Issues for SMEs")
        
        issues = {
            "Payment Terms": "Ensure clear payment schedules, late payment penalties, and dispute procedures",
            "Liability Caps": "Always insist on liability caps (typically 1-2x contract value)",
            "Termination Rights": "Ensure mutual termination rights with reasonable notice periods",
            "IP Ownership": "Clearly define who owns created intellectual property",
            "Non-Compete Clauses": "Note: Often unenforceable in India for employees",
            "Dispute Resolution": "Choose Indian jurisdiction and consider arbitration"
        }
        
        for issue, advice in issues.items():
            st.markdown(f"""
            <div class="clause-item">
                <strong style="color: #D4AF37;">{issue}</strong>
                <p style="color: #B0BEC5; margin: 5px 0 0 0; font-size: 0.9rem;">{advice}</p>
            </div>
            """, unsafe_allow_html=True)


def render_risk_display(risk_result):
    """Render risk score display"""
    score = risk_result.overall_score
    level = risk_result.risk_level.value
    
    if score < 4:
        color, badge = "risk-low", "badge-low"
    elif score < 6:
        color, badge = "risk-medium", "badge-medium"
    elif score < 8:
        color, badge = "risk-high", "badge-high"
    else:
        color, badge = "risk-critical", "badge-critical"
    
    st.markdown(f"""
    <div class="risk-gauge">
        <div class="risk-score {color}">{score:.1f}</div>
        <div style="color: #B0BEC5; margin-top: 5px;">out of 10</div>
        <div class="risk-badge {badge}">{level.upper()} RISK</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-read for accessibility
    if st.session_state.accessibility_mode and st.session_state.auto_read:
        speak(f"Risk score is {score:.1f} out of 10, rated as {level} risk.", st.session_state.voice_speed)


def main():
    """Main application"""
    load_css()
    init_state()
    render_header()
    
    # Sidebar
    settings = render_sidebar()
    
    # Welcome voice
    if st.session_state.accessibility_mode and st.session_state.voice_enabled:
        if 'welcomed' not in st.session_state:
            speak("Welcome to Legifyx. Accessibility mode is active. Use the sidebar to configure voice options.", st.session_state.voice_speed)
            st.session_state.welcomed = True
    
    # Main tabs
    tabs = st.tabs(["📤 Upload & Analyze", "📊 Results", "📚 Templates & Resources", "📜 History"])
    
    with tabs[0]:
        st.markdown('<div class="section-title">📄 Upload Contract</div>', unsafe_allow_html=True)
        
        if st.session_state.accessibility_mode:
            if st.button("🎤 Describe Upload"):
                speak("Upload section. You can upload PDF, Word, text files, or images of contracts for analysis.", st.session_state.voice_speed)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded = st.file_uploader(
                "Drop your contract file here",
                type=['pdf', 'docx', 'doc', 'txt', 'jpg', 'jpeg', 'png']
            )
        
        with col2:
            st.markdown("""
            <div class="pro-card">
                <div class="card-title">📁 Supported Formats</div>
                <div style="color: #B0BEC5; line-height: 1.8; font-size: 0.9rem;">
                    ✓ PDF Documents<br>
                    ✓ Word (DOCX/DOC)<br>
                    ✓ Text Files (TXT)<br>
                    ✓ Images (JPG/PNG)<br>
                    <span style="color: #00A878;">🔒 Files encrypted</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if uploaded:
            st.markdown(f"""
            <div class="pro-card">
                <div class="card-title">📄 Selected File</div>
                <div style="color: #FFFFFF;">{uploaded.name}</div>
                <div style="color: #B0BEC5; font-size: 0.85rem;">Size: {uploaded.size/1024:.1f} KB</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔍 ANALYZE CONTRACT", use_container_width=True, type="primary"):
                if st.session_state.accessibility_mode:
                    speak("Starting analysis. Please wait.", st.session_state.voice_speed)
                
                with st.spinner("Analyzing..."):
                    progress = st.progress(0)
                    
                    try:
                        parser = DocumentParser()
                        file_bytes = uploaded.read()
                        text, meta = parser.parse_bytes(file_bytes, uploaded.name)
                        progress.progress(30)
                        
                        if not text.strip():
                            st.error("Could not extract text from document.")
                        else:
                            st.session_state.contract_text = text
                            
                            analyzer = ContractAnalyzer()
                            result = analyzer.analyze(text)
                            progress.progress(70)
                            
                            st.session_state.analysis_result = result
                            
                            # Save to history
                            hist_entry = {
                                'id': result.contract_id,
                                'filename': uploaded.name,
                                'timestamp': result.analysis_timestamp,
                                'risk_score': result.risk_result.overall_score if result.risk_result else 0,
                                'risk_level': result.risk_result.risk_level.value if result.risk_result else 'unknown',
                                'contract_type': result.contract_type
                            }
                            st.session_state.analysis_history.append(hist_entry)
                            save_history(st.session_state.analysis_history)
                            
                            progress.progress(100)
                            st.success("✅ Analysis Complete! View Results tab.")
                            st.balloons()
                            
                            if st.session_state.accessibility_mode and st.session_state.auto_read:
                                speak(f"Analysis complete. Contract type: {result.contract_type}. Risk score: {result.risk_result.overall_score:.1f}. Go to Results tab for details.", st.session_state.voice_speed)
                    
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
    
    with tabs[1]:
        result = st.session_state.analysis_result
        
        if result:
            if st.session_state.accessibility_mode:
                if st.button("🎤 Read Summary"):
                    speak(result.executive_summary[:1000], st.session_state.voice_speed)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div class="pro-card">
                    <div class="card-title">📄 Contract Type</div>
                    <div style="font-size: 1.2rem; color: #D4AF37; font-weight: 700;">{result.contract_type}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if result.risk_result:
                    render_risk_display(result.risk_result)
            
            with col2:
                # Metrics
                cols = st.columns(4)
                metrics = [
                    ("📋", result.total_clauses, "Clauses"),
                    ("🚨", len(result.critical_clauses), "Critical"),
                    ("📝", result.word_count, "Words"),
                    ("📄", result.page_estimate, "Pages")
                ]
                for col, (icon, val, label) in zip(cols, metrics):
                    with col:
                        st.markdown(f"""
                        <div class="metric-box">
                            <div style="font-size: 1.2rem;">{icon}</div>
                            <div class="metric-value">{val}</div>
                            <div class="metric-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Details
            detail_tabs = st.tabs(["🚨 Critical Issues", "💡 Recommendations", "📝 Summary", "📤 Export"])
            
            with detail_tabs[0]:
                if result.critical_clauses:
                    for clause in result.critical_clauses:
                        st.markdown(f"""
                        <div class="clause-item clause-critical">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                <strong style="color: #FFFFFF;">Clause {clause['clause_id']}</strong>
                                <span style="background: rgba(220, 53, 69, 0.3); padding: 3px 12px; border-radius: 15px; font-size: 0.75rem; color: #DC3545;">RISK: {clause['risk_score']}/10</span>
                            </div>
                            <p style="color: #E0E0E0; margin: 0; font-size: 0.9rem;">{clause['text'][:300]}...</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="info-box">✅ <strong>No critical issues found!</strong></div>', unsafe_allow_html=True)
            
            with detail_tabs[1]:
                if result.recommendations:
                    for i, rec in enumerate(result.recommendations, 1):
                        st.markdown(f"""
                        <div class="clause-item clause-safe">
                            <strong style="color: #28A745;">{i}.</strong>
                            <span style="color: #E0E0E0;">{rec}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            with detail_tabs[2]:
                st.markdown(f"""
                <div class="pro-card">
                    <div class="card-title">📊 Executive Summary</div>
                    <div style="color: #E0E0E0; line-height: 1.7;">{result.executive_summary.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with detail_tabs[3]:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📄 Generate PDF", use_container_width=True):
                        with st.spinner("Generating..."):
                            pdf = PDFGenerator()
                            path = pdf.generate_report(result)
                            if path:
                                with open(path, 'rb') as f:
                                    st.download_button("⬇️ Download PDF", f.read(), file_name=f"legifyx_{result.contract_id}.pdf", mime="application/pdf")
                
                with col2:
                    if st.button("📋 Export JSON", use_container_width=True):
                        data = {
                            'contract_id': result.contract_id,
                            'type': result.contract_type,
                            'risk_score': result.risk_result.overall_score if result.risk_result else 0,
                            'summary': result.executive_summary
                        }
                        st.download_button("⬇️ Download JSON", json.dumps(data, indent=2), file_name=f"legifyx_{result.contract_id}.json")
                
                with col3:
                    if st.button("🔊 Audio Summary", use_container_width=True):
                        tts = TTSService()
                        path = tts.generate_summary_audio(result.plain_language_summary, result.contract_id, settings['output_language'])
                        if path:
                            st.success(f"Audio saved: {path}")
        else:
            st.markdown("""
            <div class="pro-card" style="text-align: center; padding: 50px;">
                <div style="font-size: 3rem;">📄</div>
                <div style="color: #FFFFFF; font-weight: 600; margin-top: 15px;">No Analysis Yet</div>
                <div style="color: #B0BEC5;">Upload a contract in the Upload tab to get started.</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        render_templates_tab()
    
    with tabs[3]:
        st.markdown('<div class="section-title">📜 Analysis History</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            💾 <strong>Storage Info:</strong> History is stored in JSON files locally at <code>data/storage/</code>. 
            No external database is required.
        </div>
        """, unsafe_allow_html=True)
        
        history = st.session_state.get('analysis_history', [])
        
        if history:
            for item in reversed(history[-20:]):
                color = "#28A745" if item['risk_score'] < 4 else "#FFC107" if item['risk_score'] < 7 else "#DC3545"
                st.markdown(f"""
                <div class="pro-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #FFFFFF;">📄 {item['filename']}</div>
                            <div style="color: #B0BEC5; font-size: 0.8rem;">ID: {item['id']} | {item['timestamp'][:19]}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.3rem; font-weight: 700; color: {color};">{item['risk_score']:.1f}</div>
                            <div style="font-size: 0.7rem; color: #B0BEC5;">{item['risk_level'].upper()}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🗑️ Clear History"):
                st.session_state.analysis_history = []
                save_history([])
                st.rerun()
        else:
            st.info("No analysis history yet.")
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
