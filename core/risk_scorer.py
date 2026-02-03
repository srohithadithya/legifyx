"""
Legifyx Risk Scorer
Calculates risk scores for clauses and contracts
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import re

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ClauseRiskResult:
    clause_id: int
    clause_text: str
    risk_score: float
    risk_level: RiskLevel
    risk_factors: List[Dict]
    recommendations: List[str]

@dataclass
class ContractRiskResult:
    overall_score: float
    risk_level: RiskLevel
    clause_risks: List[ClauseRiskResult]
    critical_issues: List[str]
    warnings: List[str]
    compliance_flags: List[Dict]

class RiskScorer:
    """Calculate and assess risk scores for contracts"""
    
    def __init__(self):
        self.risk_patterns = self._initialize_risk_patterns()
        self.compliance_rules = self._initialize_compliance_rules()
    
    def _initialize_risk_patterns(self) -> Dict:
        return {
            "penalty_clause": {
                "patterns": [r"penalty", r"liquidated damages", r"forfeit", r"fine\b"],
                "weight": 0.15,
                "severity": "high"
            },
            "indemnity": {
                "patterns": [r"indemnif", r"hold harmless", r"defend and indemnify"],
                "weight": 0.15,
                "severity": "high"
            },
            "unilateral_termination": {
                "patterns": [r"terminate.*without cause", r"termination at.*sole discretion"],
                "weight": 0.12,
                "severity": "high"
            },
            "unlimited_liability": {
                "patterns": [r"unlimited liability", r"no.*cap.*liability", r"without limit"],
                "weight": 0.18,
                "severity": "critical"
            },
            "auto_renewal": {
                "patterns": [r"auto.*renew", r"automatic.*renewal", r"evergreen"],
                "weight": 0.10,
                "severity": "medium"
            },
            "lock_in": {
                "patterns": [r"lock.?in", r"minimum.*term", r"commitment.*period"],
                "weight": 0.10,
                "severity": "medium"
            },
            "non_compete": {
                "patterns": [r"non.?compete", r"not.*compete", r"competitive.*restrict"],
                "weight": 0.12,
                "severity": "high"
            },
            "ip_transfer": {
                "patterns": [r"transfer.*intellectual property", r"assign.*IP", r"work.*made.*for.*hire"],
                "weight": 0.14,
                "severity": "high"
            },
            "exclusive_rights": {
                "patterns": [r"exclusive", r"sole.*rights", r"exclusivity"],
                "weight": 0.08,
                "severity": "medium"
            },
            "jurisdiction_foreign": {
                "patterns": [r"governed.*laws.*of.*(?!India)", r"jurisdiction.*outside.*India"],
                "weight": 0.10,
                "severity": "medium"
            },
            "waiver_rights": {
                "patterns": [r"waive.*right", r"waiver.*claims", r"release.*all.*claims"],
                "weight": 0.12,
                "severity": "high"
            },
            "confidentiality_perpetual": {
                "patterns": [r"confidential.*perpetuit", r"indefinite.*confidential"],
                "weight": 0.06,
                "severity": "low"
            }
        }
    
    def _initialize_compliance_rules(self) -> Dict:
        return {
            "stamp_duty": {
                "check": r"stamp duty|stamp paper|stamped",
                "required_for": ["lease", "property", "conveyance"],
                "message": "Contract may require stamp duty as per Indian Stamp Act"
            },
            "registration": {
                "check": r"registered|registration",
                "required_for": ["lease.*year", "property.*transfer", "immovable"],
                "message": "Contract may require registration under Registration Act, 1908"
            },
            "witness": {
                "check": r"witness|witnessed by",
                "required_for": ["all"],
                "message": "Consider having witnesses for enforceability"
            },
            "arbitration_clause": {
                "check": r"arbitration|arbitrator",
                "required_for": ["commercial"],
                "message": "Arbitration clause detected - verify compliance with Arbitration Act, 1996"
            }
        }
    
    def calculate_clause_risk(self, clause_text: str, clause_id: int = 0) -> ClauseRiskResult:
        """Calculate risk score for a single clause"""
        risk_factors = []
        total_weight = 0
        weighted_score = 0
        
        text_lower = clause_text.lower()
        
        for risk_name, risk_info in self.risk_patterns.items():
            for pattern in risk_info["patterns"]:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    severity_score = {"low": 3, "medium": 6, "high": 8, "critical": 10}
                    score = severity_score.get(risk_info["severity"], 5)
                    
                    risk_factors.append({
                        "type": risk_name,
                        "severity": risk_info["severity"],
                        "score": score,
                        "weight": risk_info["weight"]
                    })
                    
                    weighted_score += score * risk_info["weight"]
                    total_weight += risk_info["weight"]
                    break
        
        final_score = (weighted_score / total_weight * 10) if total_weight > 0 else 0
        final_score = min(10, max(0, final_score))
        
        risk_level = self._get_risk_level(final_score)
        recommendations = self._generate_recommendations(risk_factors)
        
        return ClauseRiskResult(
            clause_id=clause_id,
            clause_text=clause_text[:200] + "..." if len(clause_text) > 200 else clause_text,
            risk_score=round(final_score, 2),
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations
        )
    
    def calculate_contract_risk(self, clauses: List[str]) -> ContractRiskResult:
        """Calculate overall contract risk score"""
        clause_risks = []
        all_factors = []
        critical_issues = []
        warnings = []
        
        for idx, clause in enumerate(clauses):
            result = self.calculate_clause_risk(clause, idx + 1)
            clause_risks.append(result)
            all_factors.extend(result.risk_factors)
            
            if result.risk_level == RiskLevel.CRITICAL:
                critical_issues.append(f"Clause {idx + 1}: Critical risk detected")
            elif result.risk_level == RiskLevel.HIGH:
                warnings.append(f"Clause {idx + 1}: High risk - review recommended")
        
        if clause_risks:
            weights = [1.5 if r.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH] else 1.0 for r in clause_risks]
            overall_score = sum(r.risk_score * w for r, w in zip(clause_risks, weights)) / sum(weights)
        else:
            overall_score = 0
        
        compliance_flags = self._check_compliance("\n".join(clauses))
        
        return ContractRiskResult(
            overall_score=round(overall_score, 2),
            risk_level=self._get_risk_level(overall_score),
            clause_risks=clause_risks,
            critical_issues=critical_issues,
            warnings=warnings,
            compliance_flags=compliance_flags
        )
    
    def _get_risk_level(self, score: float) -> RiskLevel:
        if score >= 8:
            return RiskLevel.CRITICAL
        elif score >= 6:
            return RiskLevel.HIGH
        elif score >= 4:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    
    def _generate_recommendations(self, risk_factors: List[Dict]) -> List[str]:
        recommendations = []
        rec_map = {
            "penalty_clause": "Review penalty amounts and negotiate caps",
            "indemnity": "Limit indemnity scope and add exclusions",
            "unilateral_termination": "Negotiate mutual termination rights with notice",
            "unlimited_liability": "Add liability caps relative to contract value",
            "auto_renewal": "Add opt-out notice period before renewal",
            "non_compete": "Limit geographic scope and duration",
            "ip_transfer": "Retain ownership of pre-existing IP"
        }
        
        for factor in risk_factors:
            if factor["type"] in rec_map:
                recommendations.append(rec_map[factor["type"]])
        
        return recommendations
    
    def _check_compliance(self, text: str) -> List[Dict]:
        flags = []
        for rule_name, rule in self.compliance_rules.items():
            if not re.search(rule["check"], text, re.IGNORECASE):
                for trigger in rule["required_for"]:
                    if trigger == "all" or re.search(trigger, text, re.IGNORECASE):
                        flags.append({"rule": rule_name, "message": rule["message"]})
                        break
        return flags
