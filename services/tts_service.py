"""
Legifyx Text-to-Speech Service
Accessibility support for visually impaired users
"""

import os
from pathlib import Path
from typing import Optional
import logging
import threading

logger = logging.getLogger(__name__)


class TTSService:
    """
    Text-to-Speech service for accessibility support
    Provides voice output for visually impaired users
    """
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "audio_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.engine = None
        self.available = False
        self.rate = 150
        self.volume = 0.9
        
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            self.available = True
        except Exception as e:
            logger.warning(f"pyttsx3 not available: {e}")
            self.available = False
    
    def set_voice_properties(self, rate: int = None, volume: float = None, voice_id: str = None):
        """Set voice properties"""
        if not self.engine:
            return
        
        if rate is not None:
            self.rate = rate
            self.engine.setProperty('rate', rate)
        
        if volume is not None:
            self.volume = volume
            self.engine.setProperty('volume', volume)
        
        if voice_id is not None:
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if voice_id in voice.id:
                    self.engine.setProperty('voice', voice.id)
                    break
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if not self.engine:
            return []
        
        voices = self.engine.getProperty('voices')
        return [{'id': v.id, 'name': v.name, 'languages': v.languages} for v in voices]
    
    def speak(self, text: str):
        """Speak text immediately (blocking)"""
        if not self.available or not text:
            return
        
        try:
            # Limit text length for performance
            if len(text) > 5000:
                text = text[:5000] + "... Content truncated for audio."
            
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS speak failed: {e}")
    
    def speak_async(self, text: str):
        """Speak text in background thread (non-blocking)"""
        if not self.available:
            return
        
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    def generate_audio_file(self, text: str, filename: str) -> Optional[str]:
        """Generate audio file from text (using gTTS for MP3)"""
        try:
            from gtts import gTTS
            
            if len(text) > 10000:
                text = text[:10000] + "... Content truncated."
            
            output_path = self.output_dir / f"{filename}.mp3"
            
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
            
            return str(output_path)
        except ImportError:
            logger.warning("gTTS not available for file generation")
            return None
        except Exception as e:
            logger.error(f"Audio file generation failed: {e}")
            return None
    
    def generate_summary_audio(
        self,
        summary: str,
        contract_id: str,
        language: str = 'en'
    ) -> Optional[str]:
        """Generate audio summary for a contract analysis"""
        try:
            from gtts import gTTS
            
            filename = f"summary_{contract_id}_{language}"
            output_path = self.output_dir / f"{filename}.mp3"
            
            # Language mapping for gTTS
            lang_map = {
                'en': 'en',
                'hi': 'hi',
                'ta': 'ta',
                'te': 'te',
                'kn': 'kn',
                'ml': 'ml',
                'mr': 'mr',
                'gu': 'gu',
                'bn': 'bn',
                'pa': 'pa'
            }
            
            gtts_lang = lang_map.get(language, 'en')
            
            tts = gTTS(text=summary, lang=gtts_lang, slow=False)
            tts.save(str(output_path))
            
            return str(output_path)
        except Exception as e:
            logger.error(f"Summary audio generation failed: {e}")
            return None
    
    def generate_risk_alert_audio(self, risk_score: float, risk_level: str, critical_count: int) -> Optional[str]:
        """Generate audio alert for risk assessment"""
        alert_text = f"""
        Attention: Contract Risk Assessment Complete.
        Overall risk score is {risk_score:.1f} out of 10.
        Risk level is {risk_level}.
        {critical_count} critical clauses have been identified.
        Please review the detailed analysis for more information.
        """
        
        return self.generate_audio_file(alert_text.strip(), f"risk_alert_{int(risk_score * 10)}")
    
    def speak_navigation(self, section: str):
        """Speak navigation announcement"""
        announcements = {
            'upload': "Upload section. You can upload PDF, Word, or text files for analysis.",
            'results': "Analysis results section. View your contract analysis findings here.",
            'critical': "Critical clauses section. Review clauses that need immediate attention.",
            'recommendations': "Recommendations section. Action items to improve your contract.",
            'summary': "Contract summary section. Plain language explanation of key terms.",
            'export': "Export section. Download reports in PDF, JSON, or audio format."
        }
        
        text = announcements.get(section, f"Navigating to {section} section.")
        self.speak_async(text)
    
    def is_available(self) -> bool:
        """Check if TTS service is available"""
        return self.available
    
    def stop(self):
        """Stop current speech"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass


class AccessibilityManager:
    """
    Manager for accessibility features
    Coordinates TTS and other accessibility options
    """
    
    def __init__(self):
        self.tts = TTSService()
        self.enabled = False
        self.auto_read = False
        self.high_contrast = False
        self.large_text = False
    
    def enable(self):
        """Enable accessibility mode"""
        self.enabled = True
        self.tts.speak("Accessibility mode enabled. Voice navigation is now active.")
    
    def disable(self):
        """Disable accessibility mode"""
        self.enabled = False
    
    def announce(self, text: str):
        """Announce text if accessibility is enabled"""
        if self.enabled:
            self.tts.speak_async(text)
    
    def read_content(self, content: str):
        """Read content if auto-read is enabled"""
        if self.enabled and self.auto_read:
            self.tts.speak(content)
    
    def get_contrast_styles(self) -> dict:
        """Get high contrast styles if enabled"""
        if self.high_contrast:
            return {
                'background': '#000000',
                'text': '#FFFFFF',
                'primary': '#FFFF00',
                'secondary': '#00FFFF'
            }
        return {}
    
    def get_text_scale(self) -> float:
        """Get text scale factor if large text is enabled"""
        return 1.5 if self.large_text else 1.0
