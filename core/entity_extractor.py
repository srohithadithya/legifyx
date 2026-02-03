"""
Legifyx Entity Extractor
Extracts named entities and key data points from contracts
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Party:
    name: str
    role: str
    address: Optional[str] = None
    identifier: Optional[str] = None

@dataclass
class FinancialTerm:
    amount: str
    currency: str
    context: str
    normalized_value: Optional[float] = None

@dataclass
class DateInfo:
    date_string: str
    date_type: str
    context: str

@dataclass
class ContractEntities:
    parties: List[Party]
    dates: List[DateInfo]
    amounts: List[FinancialTerm]
    jurisdiction: Optional[str]
    governing_law: Optional[str]
    duration: Optional[str]
    obligations: List[str]
    rights: List[str]
    prohibitions: List[str]
    deliverables: List[str]
    confidentiality_terms: List[str]
    ip_clauses: List[str]

class EntityExtractor:
    """Extract structured entities from contract text"""
    
    def __init__(self):
        self.amount_pattern = r'(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:lakhs?|crores?|thousand))?'
        self.date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}'
    
    def extract_all(self, text: str) -> ContractEntities:
        """Extract all entities from contract text"""
        return ContractEntities(
            parties=self.extract_parties(text),
            dates=self.extract_dates(text),
            amounts=self.extract_amounts(text),
            jurisdiction=self.extract_jurisdiction(text),
            governing_law=self.extract_governing_law(text),
            duration=self.extract_duration(text),
            obligations=self.extract_obligations(text),
            rights=self.extract_rights(text),
            prohibitions=self.extract_prohibitions(text),
            deliverables=self.extract_deliverables(text),
            confidentiality_terms=self.extract_confidentiality(text),
            ip_clauses=self.extract_ip_clauses(text)
        )
    
    def extract_parties(self, text: str) -> List[Party]:
        """Extract contracting parties"""
        parties = []
        patterns = [
            r'(?:between|among)\s+([A-Z][A-Za-z\s,\.]+(?:Ltd|Limited|Pvt|Private|LLP|Inc)?)',
            r'"([^"]+)"\s*(?:\(hereinafter|hereinafter)',
            r'(?:First Party|Party A)[:\s]+([A-Z][A-Za-z\s,\.]+)',
            r'(?:Second Party|Party B)[:\s]+([A-Z][A-Za-z\s,\.]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.strip()
                if len(name) > 2 and name not in [p.name for p in parties]:
                    parties.append(Party(name=name, role="party"))
        
        return parties[:4]
    
    def extract_dates(self, text: str) -> List[DateInfo]:
        """Extract important dates"""
        dates = []
        contexts = {
            'effective': r'effective\s*date[:\s]+',
            'expiry': r'(?:expiry|expiration|end)\s*date[:\s]+',
            'commencement': r'commence\w*[:\s]+',
            'termination': r'terminat\w*.*date[:\s]+'
        }
        
        for date_type, context in contexts.items():
            combined = context + r'.*?(' + self.date_pattern + r')'
            for match in re.finditer(combined, text, re.IGNORECASE):
                dates.append(DateInfo(
                    date_string=match.group(1),
                    date_type=date_type,
                    context=date_type.title() + " Date"
                ))
        
        return dates
    
    def extract_amounts(self, text: str) -> List[FinancialTerm]:
        """Extract financial amounts"""
        amounts = []
        for match in re.finditer(self.amount_pattern, text, re.IGNORECASE):
            amount_str = match.group()
            start = max(0, match.start() - 50)
            context = text[start:match.start()].split()[-5:] if match.start() > 0 else []
            
            amounts.append(FinancialTerm(
                amount=amount_str,
                currency="INR",
                context=" ".join(context)
            ))
        
        return amounts[:20]
    
    def extract_jurisdiction(self, text: str) -> Optional[str]:
        """Extract jurisdiction"""
        pattern = r'(?:jurisdiction|courts? of|tribunal at)\s+([A-Za-z\s,]+?)(?:\.|,|shall)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def extract_governing_law(self, text: str) -> Optional[str]:
        """Extract governing law"""
        pattern = r'(?:governed by|laws of|subject to.*laws of)\s+([A-Za-z\s]+?)(?:\.|,|and)'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def extract_duration(self, text: str) -> Optional[str]:
        """Extract contract duration"""
        pattern = r'(?:term|duration|period)\s*(?:of|:)?\s*(\d+\s*(?:years?|months?|days?))'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def extract_obligations(self, text: str) -> List[str]:
        """Extract obligation statements"""
        pattern = r'[^.]*(?:shall|must|will|required to|obligated to)[^.]*\.'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return [m.strip() for m in matches[:15]]
    
    def extract_rights(self, text: str) -> List[str]:
        """Extract rights statements"""
        pattern = r'[^.]*(?:may|entitled to|right to|option to|permitted to)[^.]*\.'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return [m.strip() for m in matches[:15]]
    
    def extract_prohibitions(self, text: str) -> List[str]:
        """Extract prohibition statements"""
        pattern = r'[^.]*(?:shall not|must not|prohibited|forbidden|restricted from)[^.]*\.'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return [m.strip() for m in matches[:15]]
    
    def extract_deliverables(self, text: str) -> List[str]:
        """Extract deliverables"""
        pattern = r'[^.]*(?:deliver|provide|supply|furnish|submit)[^.]*\.'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return [m.strip() for m in matches[:10]]
    
    def extract_confidentiality(self, text: str) -> List[str]:
        """Extract confidentiality terms"""
        pattern = r'[^.]*(?:confidential|proprietary|trade secret|non-disclosure)[^.]*\.'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return [m.strip() for m in matches[:10]]
    
    def extract_ip_clauses(self, text: str) -> List[str]:
        """Extract IP-related clauses"""
        pattern = r'[^.]*(?:intellectual property|patent|copyright|trademark|IP rights|ownership)[^.]*\.'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return [m.strip() for m in matches[:10]]
