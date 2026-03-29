"""
"
Legifyx Contract Analyzer
Main analysis orchestrator that combines all NLP and risk assessment
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

from .nlp_engine import NLPEngine, ClauseType
from .risk_scorer import RiskScorer, RiskLevel, ContractRiskResult
from .entity_extractor import EntityExtractor, ContractEntities

@dataclass
class AnalysisResult:
    """Complete contract analysis result"""
    contract_id: str
    analysis_timestamp: str
    contract_type: str
    
    # Text metrics
    word_count: int
    page_estimate: int
    language: str
    
    # Entities
    entities: Optional[ContractEntities] = None
    
    # Risk assessment
    risk_result: Optional[ContractRiskResult] = None
    
    # Clause analysis
    total_clauses: int = 0
    clause_breakdown: Dict = field(default_factory=dict)
    
    # Key findings
    critical_clauses: List[Dict] = field(default_factory=list)
    unfavorable_terms: List[Dict] = field(default_factory=list)
    missing_clauses: List[str] = field(default_factory=list)
    ambiguous_clauses: List[Dict] = field(default_factory=list)
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    alternative_clauses: List[Dict] = field(default_factory=list)
    
    # Summary
    executive_summary: str = ""
    plain_language_summary: str = ""

class ContractAnalyzer:
    """Main contract analysis orchestrator"""
    
    def __init__(self):
        self.nlp_engine = NLPEngine()
        self.risk_scorer = RiskScorer()
        self.entity_extractor = EntityExtractor()
        
        self.contract_type_keywords = {
            "Employment Agreement": ["employee", "employer", "salary", "employment", "probation", "termination of employment"],
            "Vendor Contract": ["vendor", "supplier", "purchase order", "supply", "procurement"],
            "Lease Agreement": ["lease", "rent", "tenant", "landlord", "premises", "lessor", "lessee"],
            "Partnership Deed": ["partner", "partnership", "profit sharing", "capital contribution"],
            "Service Contract": ["service", "consultant", "contractor", "scope of work", "deliverables"],
            "Non-Disclosure Agreement": ["confidential", "non-disclosure", "NDA", "proprietary information"],
            "Franchise Agreement": ["franchise", "franchisee", "franchisor", "royalty", "territory"],
            "Distribution Agreement": ["distributor", "distribution", "territory", "reseller"],
            "License Agreement": ["license", "licensor", "licensee", "royalty", "intellectual property"]
        }
        
        self.essential_clauses = {
            "Employment Agreement": ["compensation", "termination", "notice period", "confidentiality", "non-compete"],
            "Vendor Contract": ["payment terms", "delivery", "warranty", "liability", "termination"],
            "Lease Agreement": ["rent", "security deposit", "maintenance", "termination", "renewal"],
            "Service Contract": ["scope", "payment", "timeline", "liability", "termination"]
        }
    
    def analyze(self, text: str, contract_id: str = None) -> AnalysisResult:
        """Perform complete contract analysis"""
        if not contract_id:
            contract_id = f"CONTRACT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Preprocess text
        clean_text = self.nlp_engine.preprocess_text(text)
        
        # Basic metrics
        metrics = self.nlp_engine.calculate_text_metrics(clean_text)
        language = self.nlp_engine.detect_language(clean_text)
        
        # Classify contract type
        contract_type = self._classify_contract_type(clean_text)
        
        # Extract entities
        entities = self.entity_extractor.extract_all(clean_text)
        
        # Extract and analyze clauses
        clauses = self.nlp_engine.extract_clauses(clean_text)
        clause_texts = [c.text for c in clauses]
        
        # Risk assessment
        risk_result = self.risk_scorer.calculate_contract_risk(clause_texts)
        
        # Analyze clauses by type
        clause_breakdown = self._breakdown_clauses(clauses)
        
        # Identify critical and unfavorable clauses
        critical_clauses = self._identify_critical_clauses(clauses, risk_result)
        unfavorable_terms = self._identify_unfavorable_terms(clauses)
        
        # Check for missing essential clauses
        missing_clauses = self._check_missing_clauses(clean_text, contract_type)
        
        # Detect ambiguous language
        ambiguous_clauses = self._detect_ambiguity(clauses)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_result, missing_clauses, unfavorable_terms)
        alternative_clauses = self._suggest_alternatives(unfavorable_terms)
        
        # Generate summaries
        executive_summary = self._generate_executive_summary(contract_type, risk_result, entities)
        plain_summary = self._generate_plain_summary(contract_type, entities, risk_result)
        
        return AnalysisResult(
            contract_id=contract_id,
            analysis_timestamp=datetime.now().isoformat(),
            contract_type=contract_type,
            word_count=metrics['total_words'],
            page_estimate=max(1, metrics['total_words'] // 300),
            language=language,
            entities=entities,
            risk_result=risk_result,
            total_clauses=len(clauses),
            clause_breakdown=clause_breakdown,
            critical_clauses=critical_clauses,
            unfavorable_terms=unfavorable_terms,
            missing_clauses=missing_clauses,
            ambiguous_clauses=ambiguous_clauses,
            recommendations=recommendations,
            alternative_clauses=alternative_clauses,
            executive_summary=executive_summary,
            plain_language_summary=plain_summary
        )
    
    def _classify_contract_type(self, text: str) -> str:
        """Classify the type of contract"""
        text_lower = text.lower()
        scores = {}
        
        for contract_type, keywords in self.contract_type_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in text_lower)
            scores[contract_type] = score
        
        if scores:
            best_match = max(scores, key=scores.get)
            if scores[best_match] > 0:
                return best_match
        
        return "General Contract"
    
    def _breakdown_clauses(self, clauses) -> Dict:
        """Break down clauses by type"""
        breakdown = {
            "obligations": 0,
            "rights": 0,
            "prohibitions": 0,
            "conditions": 0,
            "definitions": 0,
            "general": 0
        }
        
        for clause in clauses:
            if clause.clause_type == ClauseType.OBLIGATION:
                breakdown["obligations"] += 1
            elif clause.clause_type == ClauseType.RIGHT:
                breakdown["rights"] += 1
            elif clause.clause_type == ClauseType.PROHIBITION:
                breakdown["prohibitions"] += 1
            elif clause.clause_type == ClauseType.CONDITION:
                breakdown["conditions"] += 1
            elif clause.clause_type == ClauseType.DEFINITION:
                breakdown["definitions"] += 1
            else:
                breakdown["general"] += 1
        
        return breakdown
    
    def _identify_critical_clauses(self, clauses, risk_result) -> List[Dict]:
        """Identify clauses requiring immediate attention"""
        critical = []
        
        for clause_risk in risk_result.clause_risks:
            if clause_risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                critical.append({
                    "clause_id": clause_risk.clause_id,
                    "text": clause_risk.clause_text,
                    "risk_score": clause_risk.risk_score,
                    "risk_level": clause_risk.risk_level.value,
                    "factors": [f["type"] for f in clause_risk.risk_factors]
                })
        
        return critical
    
    def _identify_unfavorable_terms(self, clauses) -> List[Dict]:
        """Identify terms unfavorable to a typical SME"""
        unfavorable = []
        
        unfavorable_patterns = {
            "unlimited_liability": "Unlimited liability exposure",
            "unilateral_termination": "One-sided termination rights",
            "broad_indemnity": "Broad indemnification requirements",
            "ip_transfer_all": "Complete IP transfer",
            "non_compete_broad": "Overly broad non-compete",
            "exclusive_dealing": "Exclusive dealing requirements",
            "auto_renewal_long": "Long auto-renewal periods"
        }
        
        for clause in clauses:
            for indicator in clause.risk_indicators:
                if indicator in unfavorable_patterns:
                    unfavorable.append({
                        "clause_id": clause.id,
                        "text": clause.text[:150] + "...",
                        "issue": unfavorable_patterns[indicator],
                        "indicator": indicator
                    })
        
        return unfavorable
    
    def _check_missing_clauses(self, text: str, contract_type: str) -> List[str]:
        """Check for missing essential clauses"""
        missing = []
        essential = self.essential_clauses.get(contract_type, [])
        text_lower = text.lower()
        
        for clause_type in essential:
            if clause_type.lower() not in text_lower:
                missing.append(f"Missing or unclear: {clause_type.title()} clause")
        
        return missing
    
    def _detect_ambiguity(self, clauses) -> List[Dict]:
        """Detect ambiguous language in clauses"""
        ambiguous = []
        
        ambiguous_patterns = [
            (r'\b(?:reasonable|appropriate|adequate|sufficient)\b', "Subjective standard"),
            (r'\b(?:may|might|could)\s+(?:be|have)', "Uncertain outcome"),
            (r'\b(?:generally|usually|typically|normally)\b', "Non-absolute statement"),
            (r'\b(?:best efforts|reasonable efforts)\b', "Undefined effort standard"),
            (r'\b(?:as needed|as required|as appropriate)\b', "Undefined trigger")
        ]
        
        for clause in clauses:
            for pattern, issue in ambiguous_patterns:
                import re
                if re.search(pattern, clause.text, re.IGNORECASE):
                    ambiguous.append({
                        "clause_id": clause.id,
                        "text": clause.text[:100] + "...",
                        "issue": issue
                    })
                    break
        
        return ambiguous
    
    def _generate_recommendations(self, risk_result, missing, unfavorable) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on risk level
        if risk_result.risk_level == RiskLevel.CRITICAL:
            recommendations.append("⚠️ CRITICAL: Seek legal counsel before signing")
        elif risk_result.risk_level == RiskLevel.HIGH:
            recommendations.append("⚠️ HIGH RISK: Negotiate key terms before proceeding")
        
        # Based on missing clauses
        for missing_clause in missing[:3]:
            recommendations.append(f"📝 Add: {missing_clause}")
        
        # Based on unfavorable terms
        for term in unfavorable[:3]:
            recommendations.append(f"🔄 Renegotiate: {term['issue']}")
        
        # From risk scorer recommendations
        for clause_risk in risk_result.clause_risks:
            for rec in clause_risk.recommendations[:2]:
                if rec not in recommendations:
                    recommendations.append(f"💡 {rec}")
        
        return recommendations[:10]
    
    def _suggest_alternatives(self, unfavorable) -> List[Dict]:
        """Suggest alternative clause language"""
        alternatives = {
            "unlimited_liability": {
                "issue": "Unlimited Liability",
                "original": "Party shall be liable for all damages...",
                "suggested": "Party's aggregate liability shall not exceed [X] times the contract value or [specific amount], whichever is lower."
            },
            "unilateral_termination": {
                "issue": "Unilateral Termination",
                "original": "Company may terminate at its sole discretion...",
                "suggested": "Either party may terminate with [30/60/90] days written notice. Termination for cause requires written notice specifying the breach and [15] days cure period."
            },
            "broad_indemnity": {
                "issue": "Broad Indemnification",
                "original": "Party shall indemnify against all claims...",
                "suggested": "Party shall indemnify against third-party claims arising directly from Party's gross negligence or willful misconduct, subject to liability cap."
            }
        }
        
        result = []
        for term in unfavorable:
            if term["indicator"] in alternatives:
                result.append(alternatives[term["indicator"]])
        
        return result
    
    def _generate_executive_summary(self, contract_type, risk_result, entities) -> str:
        """Generate executive summary"""
        parties_str = ", ".join([p.name for p in entities.parties[:2]]) if entities.parties else "parties not identified"
        
        summary = f"""
**Contract Type:** {contract_type}
**Parties:** {parties_str}
**Overall Risk Score:** {risk_result.overall_score}/10 ({risk_result.risk_level.value.upper()})
**Critical Issues:** {len(risk_result.critical_issues)}
**Warnings:** {len(risk_result.warnings)}
**Jurisdiction:** {entities.jurisdiction or 'Not specified'}
**Duration:** {entities.duration or 'Not specified'}
        """.strip()
        
        return summary
    
    def _generate_plain_summary(self, contract_type, entities, risk_result) -> str:
        """Generate plain language summary for business owners"""
        risk_desc = {
            RiskLevel.LOW: "This contract appears relatively safe with standard terms.",
            RiskLevel.MEDIUM: "This contract has some terms that need your attention.",
            RiskLevel.HIGH: "This contract has concerning terms that could affect your business.",
            RiskLevel.CRITICAL: "This contract has serious issues. Get legal advice before signing."
        }
        
        summary = f"""
### What This Contract Is About
This is a {contract_type.lower()} between the parties mentioned.

### Risk Level
{risk_desc[risk_result.risk_level]}

### Key Things to Know
- There are {len(risk_result.critical_issues)} critical issues to address
- {len(risk_result.warnings)} items need your attention
- Duration: {entities.duration or 'Check the contract for term length'}

### What You Should Do
1. Review the highlighted clauses carefully
2. Consider negotiating the unfavorable terms
3. {"Consult a lawyer before signing" if risk_result.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] else "You may proceed with caution"}
        """.strip()
        
        return summary
