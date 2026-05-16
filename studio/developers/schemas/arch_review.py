from pydantic import BaseModel, Field, ConfigDict

class ArchReviewOutput(BaseModel):
    """Schema for architecture review output."""

    findings: list[str] = Field(
        min_length=1,
        max_length=5,
        description="Major architectural flaws (1-5 items)"
    )

    severity: str = Field(
        pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$",
        description="Overall severity level"
    )

    implications: list[str] = Field(
        description="Downstream consequences of the flaws"
    )

    action_plan: str = Field(
        max_length=500,
        description="3-sentence fix summary"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "findings": [
                    "Context injection uses naive truncation",
                    "No data contracts between agents"
                ],
                "severity": "HIGH",
                "implications": [
                    "Token waste on redundant context",
                    "Hallucination risk in agent outputs"
                ],
                "action_plan": "Implement auto-summarization with XML anchors. Define Pydantic schemas for agent outputs. Add validation in orchestrator."
            }
        }
    )
