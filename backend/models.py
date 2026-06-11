from pydantic import BaseModel, Field

class MagiRequest(BaseModel):
    context: str = Field(..., description="The sticky background state of the company/problem.")
    query: str = Field(..., description="The specific dynamic decision being asked.")

class AgentResponse(BaseModel):
    recommendation: str = Field(
        ..., 
        description="The actionable solution or recommendation."
    )
    confidence_score: int = Field(
        ..., 
        ge=0, le=100, 
        description="Confidence level from 0 to 100."
    )
    reasoning: str = Field(
        ..., 
        description="A concise 2-sentence explanation of why this path was chosen."
    )
    key_risk: str = Field(
        ..., 
        description="The biggest vulnerability or risk factor in this recommendation."
    )