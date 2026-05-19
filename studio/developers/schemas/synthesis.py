from pydantic import BaseModel, Field, ConfigDict


class SynthesisConclusion(BaseModel):
    """Single actionable conclusion from a debate synthesis."""

    decision: str = Field(
        max_length=200,
        description="What to do — concrete decision statement"
    )

    rationale: str = Field(
        max_length=300,
        description="Why — justification based on debate evidence"
    )

    implementation_steps: list[str] = Field(
        min_length=1,
        max_length=5,
        description="Concrete ordered steps to implement this decision"
    )

    risk_if_ignored: str = Field(
        max_length=200,
        description="Downstream consequence if this is not addressed"
    )


class SynthesisOutput(BaseModel):
    """Schema for debate synthesis output — structured action plan."""

    conclusions: list[SynthesisConclusion] = Field(
        min_length=1,
        max_length=5,
        description="Actionable conclusions from the panel debate (1-5)"
    )

    consensus_level: str = Field(
        pattern="^(FULL|PARTIAL|DISPUTED)$",
        description="Level of agreement between agents"
    )

    execution_order: list[str] = Field(
        description="Ordered list of conclusion decisions for execution priority"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "conclusions": [
                    {
                        "decision": "Freeze context before Pass 1 loop",
                        "rationale": "Agents reading each other's Pass 1 output breaks independent review",
                        "implementation_steps": [
                            "Snapshot context.md before loop",
                            "Pass frozen snapshot to all agents",
                            "Batch-append outputs after loop completes"
                        ],
                        "risk_if_ignored": "Echo chamber bias — agent 2 copies agent 1 conclusions"
                    }
                ],
                "consensus_level": "FULL",
                "execution_order": ["Freeze context before Pass 1 loop"]
            }
        }
    )
