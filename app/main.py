from fastapi import FastAPI, Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from .models import ModelMetadata
from .governance_engine import evaluate_compliance, get_all_logs

# Define the security scheme
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

app = FastAPI(
    title="Treasury AI Governance API",
    description="Secure endpoint for AI model compliance verification.",
    version="1.0.0"
)

SECRET_API_KEY = "treasury-secret-2026"

# Updated dependency for security
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

@app.post("/verify-model")
async def verify_model(model: ModelMetadata, api_key: str = Security(get_api_key)):
    return {"status": "success", "compliance_report": evaluate_compliance(model)}

@app.get("/audit-logs")
async def read_logs():
    return {"audit_history": get_all_logs()}