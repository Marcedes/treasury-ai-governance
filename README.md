# Treasury AI Governance Engine

## Project Overview
The Treasury AI Governance Engine is a secure, audit-ready compliance framework designed to ensure that AI models deployed within Federal financial environments adhere to the highest standards of integrity, security, and Constitutional alignment. This system utilizes a "Firmament-based" architecture—a tiered governance approach that separates foundational legal/ethical boundaries from operational performance metrics, ensuring a harmonious and compliant environment for inter-agency collaboration.

## Features
- **Firmament Gates:** Hard-coded barriers ensuring all models strictly align with the U.S. Constitution, the Rule of Law, and Federal interoperability standards.
- **Operational Compliance Scoring:** Quantitative assessment of data integrity, bias mitigation, security testing, and impact analysis.
- **Persistent Audit Logging:** Every assessment is recorded to an immutable JSON audit log, providing a transparent trail for compliance officers.
- **Secure API Access:** Robust authentication layer requiring authorized tokens for all governance interactions.

## Approach & Tools
- **Framework:** Built using FastAPI to provide a high-performance, asynchronous RESTful API.
- **Validation:** Utilizes Pydantic for strict data schema enforcement.
- **Governance Logic:** Custom-built compliance engine implementing tiered conditional logic (Hard Gates vs. Performance Scoring).
- **Persistence:** Local file-system logging (extensible to SQL-based enterprise databases).

## Assumptions
- **Infrastructure:** Assumes a Python 3.10+ runtime environment.
- **Security:** The current API Key implementation is a placeholder for enterprise-grade IAM (e.g., OAuth2, Azure Key Vault).
- **Audit Trail:** The `audit_log.json` file serves as a local development proxy for a secure, centralized Federal logging service.

## Setup & Run Instructions
**Prerequisites**
- Python 3.10+
- Git installed

**1. Clone and Setup**
```bash
git clone [https://github.com/Marcedes/treasury-ai-governance.git](https://github.com/Marcedes/treasury-ai-governance.git)
cd treasury-ai-governance
python -m venv venv