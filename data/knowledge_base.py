"""
Legifyx Knowledge Base
Stores common contract issues and best practices for Indian SMEs
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """
    Knowledge base for common contract issues faced by Indian SMEs
    Provides guidance and best practices without external legal data
    """
    
    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir) if data_dir else Path.cwd() / "data" / "knowledge_base"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.kb_file = self.data_dir / "knowledge_base.json"
        
        self.knowledge = self._initialize_knowledge()
    
    def _initialize_knowledge(self) -> Dict:
        """Initialize the knowledge base with common issues and guidance"""
        return {
            "common_issues": {
                "payment_terms": {
                    "title": "Payment Terms Issues",
                    "description": "Common problems with payment clauses in SME contracts",
                    "issues": [
                        "Unclear payment schedules",
                        "Missing late payment penalties",
                        "No provisions for disputed invoices",
                        "Lack of payment security mechanisms"
                    ],
                    "best_practices": [
                        "Specify exact payment dates or triggers",
                        "Include interest rate for late payments (max 24% p.a. per RBI guidelines)",
                        "Add dispute resolution timeline for invoice disputes",
                        "Consider advance payments or milestone-based payments"
                    ]
                },
                "termination_clauses": {
                    "title": "Termination Clause Issues",
                    "description": "Common problems with termination provisions",
                    "issues": [
                        "Unilateral termination rights favoring one party",
                        "Insufficient notice periods",
                        "Unclear termination triggers",
                        "No provisions for work-in-progress at termination"
                    ],
                    "best_practices": [
                        "Ensure mutual termination rights",
                        "Minimum 30-60 days notice for service contracts",
                        "Clear list of material breach triggers",
                        "Include transition assistance provisions"
                    ]
                },
                "liability_caps": {
                    "title": "Liability and Indemnification Issues",
                    "description": "Excessive liability exposure in contracts",
                    "issues": [
                        "Unlimited liability clauses",
                        "Broad indemnification requirements",
                        "No carve-outs for indirect damages",
                        "Asymmetric liability provisions"
                    ],
                    "best_practices": [
                        "Cap liability at 1-2x contract value or annual fees",
                        "Limit indemnity to third-party claims from gross negligence",
                        "Exclude consequential, indirect, and punitive damages",
                        "Ensure reciprocal liability terms"
                    ]
                },
                "ip_ownership": {
                    "title": "Intellectual Property Issues",
                    "description": "IP ownership and licensing concerns",
                    "issues": [
                        "Unclear ownership of created works",
                        "Overly broad IP transfers",
                        "No retention of pre-existing IP",
                        "Missing license grants for background IP"
                    ],
                    "best_practices": [
                        "Clearly define what IP is being created vs. pre-existing",
                        "Retain ownership of tools and methodologies",
                        "Grant appropriate licenses rather than full transfers",
                        "Include IP ownership upon full payment clause"
                    ]
                },
                "confidentiality": {
                    "title": "Confidentiality Issues",
                    "description": "Problems with NDA and confidentiality provisions",
                    "issues": [
                        "Perpetual confidentiality obligations",
                        "Overly broad definition of confidential information",
                        "No standard exceptions",
                        "Missing return/destruction provisions"
                    ],
                    "best_practices": [
                        "Limit confidentiality period to 3-5 years post-termination",
                        "Include standard exceptions (public knowledge, rightful possession)",
                        "Add return or destruction obligations upon termination",
                        "Ensure mutual confidentiality obligations"
                    ]
                },
                "non_compete": {
                    "title": "Non-Compete Issues",
                    "description": "Restrictive covenant concerns for SMEs",
                    "issues": [
                        "Overly broad geographic restrictions",
                        "Excessive duration of restrictions",
                        "Vague definition of competing business",
                        "No compensation for non-compete period"
                    ],
                    "best_practices": [
                        "Limit geographic scope to relevant markets",
                        "Maximum 1-2 years for most industries",
                        "Clearly define what constitutes competition",
                        "Note: Non-competes for employees may be unenforceable in India"
                    ]
                },
                "dispute_resolution": {
                    "title": "Dispute Resolution Issues",
                    "description": "Problems with conflict resolution mechanisms",
                    "issues": [
                        "Foreign jurisdiction clauses",
                        "Expensive arbitration requirements",
                        "No escalation procedure",
                        "Waiver of class action rights"
                    ],
                    "best_practices": [
                        "Choose Indian jurisdiction and governing law",
                        "Include negotiation step before arbitration",
                        "Specify a neutral arbitration seat (Mumbai/Delhi/Bangalore)",
                        "Consider fast-track arbitration for smaller disputes"
                    ]
                },
                "auto_renewal": {
                    "title": "Auto-Renewal Issues",
                    "description": "Automatic renewal and lock-in concerns",
                    "issues": [
                        "Hidden auto-renewal clauses",
                        "Short opt-out windows",
                        "Price escalation on renewal",
                        "Long lock-in periods"
                    ],
                    "best_practices": [
                        "Ensure minimum 60-90 days notice for non-renewal",
                        "Cap price increases at inflation rate or fixed percentage",
                        "Limit lock-in to 1-2 years maximum",
                        "Include ability to downgrade services"
                    ]
                }
            },
            "contract_types": {
                "employment": {
                    "essential_clauses": [
                        "Job description and responsibilities",
                        "Compensation and benefits",
                        "Working hours and leave policy",
                        "Probation period and confirmation",
                        "Notice period for both parties",
                        "Confidentiality obligations",
                        "Intellectual property assignment",
                        "Termination grounds"
                    ],
                    "watch_out_for": [
                        "Overly broad non-compete (often unenforceable in India)",
                        "Unclear variable pay calculations",
                        "One-sided termination clauses",
                        "Missing leave encashment provisions"
                    ]
                },
                "vendor": {
                    "essential_clauses": [
                        "Scope of goods/services",
                        "Pricing and payment terms",
                        "Delivery schedule and acceptance",
                        "Quality standards and warranties",
                        "Liability and indemnification",
                        "Termination provisions",
                        "Force majeure"
                    ],
                    "watch_out_for": [
                        "Unlimited liability exposure",
                        "Unclear acceptance criteria",
                        "No right to audit",
                        "Automatic price escalation"
                    ]
                },
                "lease": {
                    "essential_clauses": [
                        "Property description and permitted use",
                        "Rent and security deposit",
                        "Maintenance responsibilities",
                        "Lease term and renewal options",
                        "Termination and notice requirements",
                        "Alterations and improvements",
                        "Insurance requirements"
                    ],
                    "watch_out_for": [
                        "Excessive security deposit (>6 months)",
                        "Arbitrary rent escalation",
                        "Lessor's unilateral termination rights",
                        "Improvement ownership clauses"
                    ]
                },
                "service": {
                    "essential_clauses": [
                        "Scope of services and deliverables",
                        "Service levels and KPIs",
                        "Pricing and payment terms",
                        "Term and termination",
                        "Intellectual property rights",
                        "Confidentiality",
                        "Liability limitations",
                        "Dispute resolution"
                    ],
                    "watch_out_for": [
                        "Vague scope leading to scope creep",
                        "Unrealistic SLAs with heavy penalties",
                        "Full IP transfer without fair compensation",
                        "Broad indemnification requirements"
                    ]
                }
            },
            "indian_law_notes": {
                "contract_act": {
                    "title": "Indian Contract Act, 1872",
                    "key_points": [
                        "Contracts must have lawful consideration and object",
                        "Agreements in restraint of trade are void (Section 27)",
                        "Penalty clauses may be reduced to reasonable amounts (Section 74)",
                        "Minor cannot be a party to a contract"
                    ]
                },
                "stamp_act": {
                    "title": "Indian Stamp Act",
                    "key_points": [
                        "Many agreements require stamp duty",
                        "Rates vary by state and document type",
                        "Unstamped documents may not be admissible as evidence",
                        "E-stamping available in most states"
                    ]
                },
                "arbitration_act": {
                    "title": "Arbitration and Conciliation Act, 1996",
                    "key_points": [
                        "Parties can choose arbitration over court litigation",
                        "Arbitration agreements must be in writing",
                        "Awards are enforceable like court decrees",
                        "Limited grounds for challenging arbitration awards"
                    ]
                },
                "it_act": {
                    "title": "Information Technology Act, 2000",
                    "key_points": [
                        "Electronic contracts are valid and enforceable",
                        "Digital signatures have legal validity",
                        "Certain documents still require physical signature",
                        "Data protection obligations for handling personal data"
                    ]
                }
            },
            "red_flags": {
                "critical": [
                    "Unlimited liability without caps",
                    "Unilateral termination without cause by other party",
                    "Complete IP transfer including pre-existing IP",
                    "Foreign jurisdiction with no Indian recourse",
                    "Personal guarantees for company obligations",
                    "Waiver of statutory rights"
                ],
                "warning": [
                    "Auto-renewal with short opt-out window",
                    "Broad indemnification beyond gross negligence",
                    "Non-compete exceeding 2 years",
                    "Penalty clauses exceeding 2x contract value",
                    "One-sided force majeure provisions",
                    "Audit rights without reasonable notice"
                ],
                "caution": [
                    "Vague deliverable descriptions",
                    "Payment terms exceeding 60 days",
                    "Minimum commitment periods",
                    "Anti-assignment without consent",
                    "Broad definition of confidential information"
                ]
            }
        }
    
    def get_common_issues(self, category: str = None) -> Dict:
        """Get common contract issues"""
        if category:
            return self.knowledge["common_issues"].get(category, {})
        return self.knowledge["common_issues"]
    
    def get_contract_type_guidance(self, contract_type: str) -> Dict:
        """Get guidance for specific contract type"""
        type_map = {
            "employment agreement": "employment",
            "vendor contract": "vendor",
            "lease agreement": "lease",
            "service contract": "service"
        }
        key = type_map.get(contract_type.lower(), contract_type.lower())
        return self.knowledge["contract_types"].get(key, {})
    
    def get_red_flags(self, severity: str = None) -> List[str]:
        """Get red flag indicators"""
        if severity:
            return self.knowledge["red_flags"].get(severity, [])
        return self.knowledge["red_flags"]
    
    def get_indian_law_notes(self, law: str = None) -> Dict:
        """Get Indian law reference notes"""
        if law:
            return self.knowledge["indian_law_notes"].get(law, {})
        return self.knowledge["indian_law_notes"]
    
    def search(self, query: str) -> List[Dict]:
        """Search knowledge base for relevant information"""
        results = []
        query_lower = query.lower()
        
        # Search common issues
        for key, issue in self.knowledge["common_issues"].items():
            if query_lower in issue["title"].lower() or query_lower in issue["description"].lower():
                results.append({
                    "type": "common_issue",
                    "key": key,
                    "content": issue
                })
        
        # Search red flags
        for severity, flags in self.knowledge["red_flags"].items():
            for flag in flags:
                if query_lower in flag.lower():
                    results.append({
                        "type": "red_flag",
                        "severity": severity,
                        "content": flag
                    })
        
        return results
    
    def export_knowledge_base(self, output_path: str = None) -> str:
        """Export knowledge base to JSON file"""
        if not output_path:
            output_path = self.data_dir / f"kb_export_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(output_path, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
        
        return str(output_path)
