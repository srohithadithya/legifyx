"""
Legifyx Translation Service
Handles multilingual translation and normalization
Compatible with Python 3.9 - 3.12
"""

from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TranslationService:
    """Handle multilingual translation for contracts"""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'bn': 'Bengali',
        'pa': 'Punjabi'
    }
    
    def __init__(self):
        self.translator_available = False
        self._init_translator()
    
    def _init_translator(self):
        """Initialize translation backend"""
        try:
            from deep_translator import GoogleTranslator
            self.GoogleTranslator = GoogleTranslator
            self.translator_available = True
        except ImportError:
            logger.warning("deep-translator not available. Install with: pip install deep-translator")
            self.translator_available = False
    
    def detect_language(self, text: str) -> str:
        """Detect the language of text"""
        try:
            from langdetect import detect
            return detect(text[:1000])  # Limit text for speed
        except:
            return 'en'
    
    def translate(self, text: str, target_lang: str = 'en', source_lang: str = None) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (auto-detect if None)
        
        Returns:
            Translated text
        """
        if not self.translator_available:
            return text
        
        if not text or not text.strip():
            return text
        
        try:
            # Detect source language if not provided
            if not source_lang:
                source_lang = self.detect_language(text)
            
            # Skip if same language
            if source_lang == target_lang:
                return text
            
            # Handle long text by chunking
            max_chunk = 4500
            if len(text) > max_chunk:
                chunks = []
                current_chunk = ""
                
                for sentence in text.split('. '):
                    if len(current_chunk) + len(sentence) < max_chunk:
                        current_chunk += sentence + '. '
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + '. '
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                translated_chunks = []
                for chunk in chunks:
                    translator = self.GoogleTranslator(source=source_lang, target=target_lang)
                    result = translator.translate(chunk)
                    translated_chunks.append(result)
                
                return ' '.join(translated_chunks)
            else:
                translator = self.GoogleTranslator(source=source_lang, target=target_lang)
                return translator.translate(text)
                
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text
    
    def normalize_to_english(self, text: str) -> str:
        """Normalize non-English text to English for NLP processing"""
        detected = self.detect_language(text)
        
        if detected != 'en':
            return self.translate(text, target_lang='en', source_lang=detected)
        
        return text
    
    def get_summary_in_language(self, summary: str, target_lang: str) -> str:
        """Get summary in specified language"""
        if target_lang == 'en':
            return summary
        
        return self.translate(summary, target_lang=target_lang, source_lang='en')
    
    def translate_key_terms(self, terms: Dict[str, str], target_lang: str) -> Dict[str, str]:
        """Translate key legal terms to target language"""
        if target_lang == 'en':
            return terms
        
        translated = {}
        for key, value in terms.items():
            translated[key] = self.translate(value, target_lang=target_lang)
        
        return translated
    
    def is_available(self) -> bool:
        """Check if translation service is available"""
        return self.translator_available
