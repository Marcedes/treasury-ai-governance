from pydantic import BaseModel, Field

class ModelMetadata(BaseModel):
    model_name: str
    purpose: str
    sensitivity_level: str = Field("Confidential", description="Public, Internal, or Confidential")
    
    # Firmament Gates
    constitutional_alignment: bool = Field(..., description="Confirm alignment with US Constitutional principles")
    rule_of_law_adherence: bool = Field(..., description="Confirm adherence to Federal regulations and rule of law")
    cross_agency_standards_met: bool = Field(..., description="Ensures interoperability and harmony with Federal partners")
    
    # Operational Criteria
    data_source_integrity_verified: bool
    bias_mitigation_performed: bool
    security_testing_completed: bool
    stakeholder_impact_analysis: bool