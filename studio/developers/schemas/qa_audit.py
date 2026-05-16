from pydantic import BaseModel, Field

class QAAuditOutput(BaseModel):
    """Schema for GOONER_AUDIT_FRAMEWORK evaluation."""

    f_score: int = Field(
        ge=0, le=20,
        description="F-Score (Cultural Fidelity/Fetish Logic)"
    )

    s_score: int = Field(
        ge=0, le=20,
        description="S-Score (Sensory Density)"
    )

    p_score: int = Field(
        ge=0, le=20,
        description="P-Score (Prose Quality)"
    )

    i_score: int = Field(
        ge=0, le=20,
        description="I-Score (In-Character/Identity)"
    )

    total_score: int = Field(
        ge=0, le=100,
        description="Total Score (Sum of scores)"
    )

    verdict: str = Field(
        pattern="^(PASS|FAIL|REWRITE)$",
        description="Final audit verdict"
    )

    critical_flaws: list[str] = Field(
        description="List of issues that failed the quality gate"
    )

    action_plan: str = Field(
        max_length=500,
        description="Required fixes for the next iteration"
    )
