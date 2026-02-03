"""
Legifyx Clause Templates
Standard clause templates for SME-friendly contracts
"""

CLAUSE_TEMPLATES = {
    "liability_cap": {
        "name": "Liability Cap Clause",
        "category": "liability",
        "risk_level": "low",
        "template": """
LIMITATION OF LIABILITY

{party_a}'s aggregate liability under this Agreement, whether in contract, tort (including negligence), or otherwise, shall not exceed {liability_cap}.

Neither party shall be liable to the other for any indirect, incidental, special, consequential, or punitive damages, including but not limited to loss of profits, revenue, data, or business opportunities, even if advised of the possibility of such damages.

The limitations in this section shall not apply to:
(a) Breaches of confidentiality obligations;
(b) Intellectual property infringement;
(c) Gross negligence or willful misconduct; or
(d) Payment obligations under this Agreement.
""",
        "variables": ["party_a", "liability_cap"],
        "guidance": "Liability cap is typically set at 1-2x the annual contract value."
    },
    
    "mutual_termination": {
        "name": "Mutual Termination Clause",
        "category": "termination",
        "risk_level": "low",
        "template": """
TERMINATION

1. Termination for Convenience: Either party may terminate this Agreement without cause by providing {notice_period} days' written notice to the other party.

2. Termination for Cause: Either party may terminate this Agreement immediately upon written notice if:
   (a) The other party materially breaches this Agreement and fails to cure such breach within {cure_period} days of receiving written notice; or
   (b) The other party becomes insolvent, files for bankruptcy, or makes an assignment for the benefit of creditors.

3. Effect of Termination: Upon termination:
   (a) All outstanding payments shall become due within {payment_due_days} days;
   (b) Each party shall return or destroy the other party's Confidential Information;
   (c) Provisions that by their nature should survive shall survive termination.
""",
        "variables": ["notice_period", "cure_period", "payment_due_days"],
        "guidance": "Notice period of 30-60 days and cure period of 15-30 days are standard."
    },
    
    "balanced_indemnity": {
        "name": "Balanced Indemnification Clause",
        "category": "indemnity",
        "risk_level": "low",
        "template": """
INDEMNIFICATION

1. {party_a} Indemnification: {party_a} shall indemnify, defend, and hold harmless {party_b} from and against any third-party claims, damages, losses, and expenses (including reasonable attorneys' fees) arising from:
   (a) {party_a}'s gross negligence or willful misconduct; or
   (b) {party_a}'s breach of its representations and warranties under this Agreement.

2. {party_b} Indemnification: {party_b} shall indemnify, defend, and hold harmless {party_a} from and against any third-party claims, damages, losses, and expenses (including reasonable attorneys' fees) arising from:
   (a) {party_b}'s gross negligence or willful misconduct; or
   (b) {party_b}'s breach of its representations and warranties under this Agreement.

3. Indemnification Cap: Each party's indemnification obligations shall be subject to the liability limitations set forth in this Agreement.

4. Procedure: The indemnified party shall promptly notify the indemnifying party of any claim and provide reasonable cooperation.
""",
        "variables": ["party_a", "party_b"],
        "guidance": "Indemnity should be mutual and limited to third-party claims from gross negligence."
    },
    
    "fair_ip_ownership": {
        "name": "Fair IP Ownership Clause",
        "category": "intellectual_property",
        "risk_level": "low",
        "template": """
INTELLECTUAL PROPERTY RIGHTS

1. Pre-Existing IP: Each party retains all rights in its pre-existing intellectual property, including tools, methodologies, frameworks, and know-how.

2. Work Product: Subject to full payment of all fees, {party_a} hereby assigns to {party_b} all rights, title, and interest in the Work Product specifically created for {party_b} under this Agreement.

3. License to Pre-Existing IP: {party_a} grants {party_b} a non-exclusive, perpetual, royalty-free license to use any of {party_a}'s pre-existing intellectual property that is incorporated into the Work Product, solely as necessary for {party_b} to use the Work Product.

4. Feedback: Any feedback provided by {party_b} may be used by {party_a} without restriction or compensation.

5. IP Upon Non-Payment: If {party_b} fails to pay any undisputed invoice within {payment_days} days of its due date, the assignment in Section 2 shall not take effect until full payment is received.
""",
        "variables": ["party_a", "party_b", "payment_days"],
        "guidance": "Service provider should retain pre-existing IP; work product transfers upon payment."
    },
    
    "reasonable_confidentiality": {
        "name": "Reasonable Confidentiality Clause",
        "category": "confidentiality",
        "risk_level": "low",
        "template": """
CONFIDENTIALITY

1. Definition: "Confidential Information" means any non-public information disclosed by one party to the other that is designated as confidential or that reasonably should be understood to be confidential.

2. Obligations: Each party shall:
   (a) Maintain the confidentiality of the other party's Confidential Information;
   (b) Use such information only for purposes of this Agreement;
   (c) Limit disclosure to employees and contractors with a need to know.

3. Exceptions: Confidential Information does not include information that:
   (a) Is or becomes publicly available through no fault of the receiving party;
   (b) Was rightfully in the receiving party's possession prior to disclosure;
   (c) Is rightfully obtained from a third party without restriction;
   (d) Is independently developed without use of Confidential Information; or
   (e) Is required to be disclosed by law (with prompt notice to the disclosing party).

4. Duration: Confidentiality obligations shall survive termination for {confidentiality_period} years.

5. Return of Information: Upon termination or request, each party shall return or destroy the other party's Confidential Information and certify such destruction.
""",
        "variables": ["confidentiality_period"],
        "guidance": "3-5 years is reasonable; perpetual confidentiality is often excessive."
    },
    
    "indian_arbitration": {
        "name": "Indian Arbitration Clause",
        "category": "dispute_resolution",
        "risk_level": "low",
        "template": """
DISPUTE RESOLUTION

1. Negotiation: The parties shall attempt in good faith to resolve any dispute arising out of or relating to this Agreement through negotiation between senior executives of each party. If the dispute is not resolved within {negotiation_days} days, either party may proceed to arbitration.

2. Arbitration: Any dispute not resolved through negotiation shall be finally settled by binding arbitration in accordance with the Arbitration and Conciliation Act, 1996, as amended.

3. Arbitration Procedure:
   (a) The arbitration shall be conducted by a sole arbitrator mutually agreed upon by the parties. If the parties cannot agree within {arbitrator_selection_days} days, the arbitrator shall be appointed by {appointing_authority}.
   (b) The seat of arbitration shall be {arbitration_seat}, India.
   (c) The language of arbitration shall be English.
   (d) The arbitrator's decision shall be final and binding on both parties.

4. Governing Law: This Agreement shall be governed by and construed in accordance with the laws of India.

5. Jurisdiction: Subject to the arbitration clause above, the courts of {jurisdiction_city} shall have exclusive jurisdiction.

6. Continued Performance: During the pendency of any dispute, the parties shall continue to perform their respective obligations under this Agreement.
""",
        "variables": ["negotiation_days", "arbitrator_selection_days", "appointing_authority", "arbitration_seat", "jurisdiction_city"],
        "guidance": "Choose a major city (Mumbai, Delhi, Bangalore) for arbitration seat."
    },
    
    "fair_auto_renewal": {
        "name": "Fair Auto-Renewal Clause",
        "category": "term",
        "risk_level": "low",
        "template": """
TERM AND RENEWAL

1. Initial Term: This Agreement shall commence on the Effective Date and continue for an initial term of {initial_term} unless terminated earlier in accordance with this Agreement.

2. Renewal: This Agreement shall automatically renew for successive {renewal_term} periods unless either party provides written notice of non-renewal at least {non_renewal_notice} days prior to the end of the then-current term.

3. Price Adjustment: Upon each renewal, the fees may be adjusted by a maximum of {max_increase}% or the change in the Consumer Price Index, whichever is lower. Any price increase shall be communicated at least {price_notice_days} days before the renewal date.

4. No Lock-In: After the initial term, either party may terminate this Agreement at any time with {termination_notice} days' written notice.
""",
        "variables": ["initial_term", "renewal_term", "non_renewal_notice", "max_increase", "price_notice_days", "termination_notice"],
        "guidance": "Non-renewal notice of 60-90 days is reasonable; price increases should be capped."
    },
    
    "payment_terms": {
        "name": "Payment Terms Clause",
        "category": "payment",
        "risk_level": "low",
        "template": """
PAYMENT TERMS

1. Fees: {party_b} shall pay {party_a} the fees as set forth in the applicable Statement of Work or Exhibit.

2. Invoicing: {party_a} shall submit invoices {invoicing_frequency}. Each invoice shall include sufficient detail of the services performed.

3. Payment Due: Payment shall be due within {payment_days} days of receipt of a valid invoice.

4. Late Payment: Late payments shall bear interest at the rate of {interest_rate}% per month or the maximum rate permitted by law, whichever is lower.

5. Disputed Invoices: If {party_b} disputes any portion of an invoice, {party_b} shall:
   (a) Pay the undisputed portion by the due date;
   (b) Notify {party_a} of the disputed amount with reasons within {dispute_notice_days} days of invoice receipt;
   (c) Work in good faith to resolve the dispute within {dispute_resolution_days} days.

6. Taxes: All fees are exclusive of applicable taxes. {party_b} shall pay all applicable GST and other taxes.

7. No Set-Off: {party_b} shall not set off any amounts owed to {party_a} against claims for damages or other amounts.
""",
        "variables": ["party_a", "party_b", "invoicing_frequency", "payment_days", "interest_rate", "dispute_notice_days", "dispute_resolution_days"],
        "guidance": "Payment terms of 30-45 days are standard; interest rate should comply with RBI guidelines."
    }
}


def get_template(template_name: str) -> dict:
    """Get a specific clause template"""
    return CLAUSE_TEMPLATES.get(template_name, {})


def get_templates_by_category(category: str) -> list:
    """Get all templates in a category"""
    return [t for t in CLAUSE_TEMPLATES.values() if t.get("category") == category]


def get_all_templates() -> dict:
    """Get all available templates"""
    return CLAUSE_TEMPLATES


def fill_template(template_name: str, variables: dict) -> str:
    """Fill a template with provided variables"""
    template = CLAUSE_TEMPLATES.get(template_name, {})
    if not template:
        return ""
    
    text = template.get("template", "")
    for var, value in variables.items():
        text = text.replace(f"{{{var}}}", str(value))
    
    return text.strip()
