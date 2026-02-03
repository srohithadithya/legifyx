"""
Legifyx NLP Engine
Core natural language processing for contract analysis
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# Try to import NLP libraries
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("spaCy not available")

try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
    
    # Download required data
    for resource in ['punkt', 'stopwords', 'averaged_perceptron_tagger']:
        try:
            nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}' if resource == 'stopwords' else f'taggers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)
except ImportError:
    NLTK_AVAILABLE = False
    logger.warning("NLTK not available")


class ClauseType(Enum):
    """Types of clauses in a contract"""
    OBLIGATION = "obligation"
    RIGHT = "right"
    PROHIBITION = "prohibition"
    CONDITION = "condition"
    DEFINITION = "definition"
    GENERAL = "general"


@dataclass
class ExtractedClause:
    """Represents an extracted clause from the contract"""
    id: int
    text: str
    clause_type: ClauseType
    section: str
    start_pos: int
    end_pos: int
    entities: List[Dict]
    risk_indicators: List[str]
    confidence: float


class NLPEngine:
    """
    Core NLP engine for contract analysis
    Handles text processing, entity extraction, and clause classification
    """
    
    def __init__(self):
        """Initialize the NLP engine"""
        self.nlp = None
        
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_lg")
            except OSError:
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                except OSError:
                    logger.warning("No spaCy model available")
        
        self.stop_words = set()
        if NLTK_AVAILABLE:
            try:
                self.stop_words = set(stopwords.words('english'))
            except:
                pass
        
        # Pattern definitions
        self.obligation_patterns = [
            r'\bshall\b', r'\bmust\b', r'\bwill\b', r'\brequired\b',
            r'\bobligated\b', r'\bresponsible\b', r'\bensure\b'
        ]
        
        self.right_patterns = [
            r'\bmay\b', r'\bentitled\b', r'\bright\b', r'\boption\b',
            r'\bpermitted\b', r'\bauthorized\b', r'\ballowed\b'
        ]
        
        self.prohibition_patterns = [
            r'\bshall not\b', r'\bwill not\b', r'\bmust not\b',
            r'\bprohibited\b', r'\bforbidden\b', r'\brestricted\b'
        ]
        
        self.amount_patterns = [
            r'(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:lakhs?|crores?|thousand))?',
            r'[\d,]+(?:\.\d{2})?\s*(?:Rs\.?|INR|₹)',
        ]
        
        self.date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess contract text"""
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = re.sub(r'Page\s*\d+\s*of\s*\d+', '', text, flags=re.IGNORECASE)
        return text.strip()
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from contract text"""
        text = self.preprocess_text(text)
        
        if NLTK_AVAILABLE:
            sentences = sent_tokenize(text)
        else:
            sentences = re.split(r'[.!?]+', text)
        
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def extract_clauses(self, text: str) -> List[ExtractedClause]:
        """Extract and classify clauses from contract text"""
        clauses = []
        
        # Split by common clause patterns
        clause_pattern = r'(?:^|\n)\s*(?:(\d+(?:\.\d+)*)\s*[.):]?\s*|(?:Article|Section|Clause)\s+(\d+(?:\.\d+)*)[.:]\s*)'
        parts = re.split(clause_pattern, text, flags=re.MULTILINE | re.IGNORECASE)
        
        current_section = "General"
        clause_id = 0
        
        for part in parts:
            if part is None or not part.strip():
                continue
            
            if re.match(r'^\d+(?:\.\d+)*$', part.strip()):
                current_section = part.strip()
                continue
            
            clause_text = part.strip()
            if len(clause_text) < 20:
                continue
            
            clause_id += 1
            clause_type = self._classify_clause_type(clause_text)
            entities = self._extract_entities_from_text(clause_text)
            risk_indicators = self._identify_risk_indicators(clause_text)
            
            clause = ExtractedClause(
                id=clause_id,
                text=clause_text,
                clause_type=clause_type,
                section=current_section,
                start_pos=text.find(clause_text),
                end_pos=text.find(clause_text) + len(clause_text),
                entities=entities,
                risk_indicators=risk_indicators,
                confidence=0.85
            )
            clauses.append(clause)
        
        return clauses
    
    def _classify_clause_type(self, text: str) -> ClauseType:
        """Classify the type of a clause"""
        text_lower = text.lower()
        
        for pattern in self.prohibition_patterns:
            if re.search(pattern, text_lower):
                return ClauseType.PROHIBITION
        
        for pattern in self.obligation_patterns:
            if re.search(pattern, text_lower):
                return ClauseType.OBLIGATION
        
        for pattern in self.right_patterns:
            if re.search(pattern, text_lower):
                return ClauseType.RIGHT
        
        if re.search(r'"[^"]+"\s*(?:means|refers to|shall mean)', text_lower):
            return ClauseType.DEFINITION
        
        if re.search(r'\b(?:if|unless|provided that|subject to)\b', text_lower):
            return ClauseType.CONDITION
        
        return ClauseType.GENERAL
    
    def _extract_entities_from_text(self, text: str) -> List[Dict]:
        """Extract named entities from text"""
        entities = []
        
        if self.nlp:
            doc = self.nlp(text[:5000])  # Limit for performance
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'type': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        # Custom patterns
        for pattern in self.amount_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(),
                    'type': 'AMOUNT',
                    'start': match.start(),
                    'end': match.end()
                })
        
        for pattern in self.date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(),
                    'type': 'DATE',
                    'start': match.start(),
                    'end': match.end()
                })
        
        return entities
    
    def _identify_risk_indicators(self, text: str) -> List[str]:
        """Identify risk indicators in text"""
        risk_indicators = []
        text_lower = text.lower()
        
        patterns = {
            'penalty': r'\b(?:penalty|fine|damages|liquidated damages)\b',
            'indemnity': r'\b(?:indemnify|indemnification|hold harmless)\b',
            'unilateral_termination': r'\b(?:terminate.*without.*cause|at.*sole.*discretion)\b',
            'unlimited_liability': r'\b(?:unlimited liability|no cap|without limit)\b',
            'auto_renewal': r'\b(?:auto-?renew|automatic.*renew)\b',
            'non_compete': r'\b(?:non-?compete|not.*compete)\b',
            'ip_transfer': r'\b(?:transfer.*intellectual property|assign.*IP)\b'
        }
        
        for indicator, pattern in patterns.items():
            if re.search(pattern, text_lower):
                risk_indicators.append(indicator)
        
        return risk_indicators
    
    def extract_parties(self, text: str) -> List[Dict]:
        """Extract contracting parties"""
        parties = []
        
        patterns = [
            r'(?:between|among)\s+([A-Z][A-Za-z\s,]+(?:Ltd|Limited|Pvt|Private|LLP)?)',
            r'"([^"]+)"\s*(?:\(hereinafter|hereinafter)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.strip()
                if len(name) > 2 and name not in [p['name'] for p in parties]:
                    parties.append({'name': name, 'role': 'party'})
        
        return parties[:5]
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return 'en'
    
    def calculate_text_metrics(self, text: str) -> Dict:
        """Calculate various text metrics"""
        if NLTK_AVAILABLE:
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
        else:
            sentences = re.split(r'[.!?]+', text)
            words = text.split()
        
        sentences = [s for s in sentences if s.strip()]
        words = [w for w in words if w.strip()]
        
        return {
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_sentence_length': round(len(words) / max(1, len(sentences)), 2),
            'estimated_reading_time_minutes': round(len(words) / 200, 1)
        }
