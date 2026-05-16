from pydantic import BaseModel, Field, ConfigDict

class CodeReviewIssue(BaseModel):
    """Single code review issue."""

    line: int | None = Field(
        default=None,
        description="Line number (if applicable)"
    )

    severity: str = Field(
        pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$",
        description="Issue severity"
    )

    category: str = Field(
        description="Issue category: slop, sensory_density, fetish_accuracy, pacing, format"
    )

    description: str = Field(
        max_length=200,
        description="Issue description"
    )

    suggested_rewrite: str | None = Field(
        default=None,
        description="Suggested fix (if applicable)"
    )

class CodeReviewOutput(BaseModel):
    """Schema for code/prose review output."""

    issues: list[CodeReviewIssue] = Field(
        description="List of identified issues"
    )

    overall_score: int = Field(
        ge=0,
        le=100,
        description="Overall quality score (0-100)"
    )

    verdict: str = Field(
        pattern="^(PASS|FAIL|REWRITE)$",
        description="Final verdict"
    )

    summary: str = Field(
        max_length=300,
        description="Brief summary of review"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "issues": [
                    {
                        "line": 42,
                        "severity": "HIGH",
                        "category": "slop",
                        "description": "Generic phrase 'a mix of fear and excitement'",
                        "suggested_rewrite": "Her breath caught—arousal spiking through dread."
                    }
                ],
                "overall_score": 65,
                "verdict": "REWRITE",
                "summary": "Prose has good pacing but contains AI slop phrases. Sensory density is adequate. Needs rewrite to remove generic tropes."
            }
        }
    )
