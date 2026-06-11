import json
import os
from .models import ModelMetadata

REMEDIATION_GUIDE = {
    "Data Integrity not verified": "Run data_audit_script.py on source bucket.",
    "Bias mitigation missing": "Execute fairness_check.ipynb to identify skew.",
    "Security testing incomplete": "Contact InfoSec for penetration test window.",
    "Impact analysis missing": "Complete the 'Treasury_Impact_Assessment_Template.docx'.",
    "Firmament Failure": "Ensure model adheres to US Constitution, Rule of Law, and Federal Interoperability standards."
}

def get_all_logs():
    if not os.path.exists("audit_log.json"): return []
    with open("audit_log.json", "r") as f:
        return [json.loads(line) for line in f]

def evaluate_compliance(model: ModelMetadata):
    # 1. The Firmament Gates (Constitutional & Harmony Checks)
    if not (model.constitutional_alignment and model.rule_of_law_adherence and model.cross_agency_standards_met):
        return {
            "model_name": model.model_name,
            "is_compliant": False,
            "remediation_steps": [REMEDIATION_GUIDE["Firmament Failure"]]
        }

    # 2. Operational Scoring
    score = 0
    failures = []
    criteria = [
        (model.data_source_integrity_verified, "Data Integrity not verified"),
        (model.bias_mitigation_performed, "Bias mitigation missing"),
        (model.security_testing_completed, "Security testing incomplete"),
        (model.stakeholder_impact_analysis, "Impact analysis missing")
    ]
    
    for passed, message in criteria:
        if passed: score += 25
        else: failures.append(message)
        
    # Confidentiality Constraint
    is_compliant = (score >= 75) and not (model.sensitivity_level == "Confidential" and not model.security_testing_completed)
    
    report = {
        "model_name": model.model_name,
        "compliance_score": score,
        "is_compliant": is_compliant,
        "remediation_steps": [REMEDIATION_GUIDE[f] for f in failures]
    }
    
    # Audit Logging
    with open("audit_log.json", "a") as f:
        f.write(json.dumps(report) + "\n")
        
    return report