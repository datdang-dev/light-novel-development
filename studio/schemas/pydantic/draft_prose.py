from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class SensoryAffect(BaseModel):
    """Structured sensory and physiological affect markers for R18 prose."""
    
    olfactory: list[str] = Field(
        description="Olfactory triggers included in the scene (e.g. sweat, semen scent, secretions, clothing aroma)."
    )
    tactile: list[str] = Field(
        description="Tactile sensations described (e.g. temperature, wetness, friction, pressure, viscosity)."
    )
    visual: list[str] = Field(
        description="Visual physiological reactions (e.g. flushing, trembling, eye-rolling, heavy panting)."
    )
    dialogue_escalation: str = Field(
        description="Dirty talk and vocal escalation level. E.g., MANIC, WHISPER, SUBMISSIVE, TSUN-TSUN, EXPLICIT."
    )
    tsundere_breakdown: float = Field(
        ge=0.0, le=10.0,
        description="Tsundere cognitive dissonance rating from 0.0 (stoic, highly resistant) to 10.0 (complete submission/emotional breakdown)."
    )
    stroking_metric: int = Field(
        ge=0, le=10,
        description="Physiological arousal intensity score from 0 to 10 (evaluates how stroke-inducing the section is)."
    )

class FormatCompliance(BaseModel):
    has_header: bool
    has_footer: bool
    valid_dialogue_format: bool
    valid_sfx_format: bool

class LegacyMetrics(BaseModel):
    smell_mentions: int
    sound_mentions: int
    texture_mentions: int
    temperature_mentions: int

class DraftProseOutput(BaseModel):
    """Advanced schema for draft prose outputs with sensory and affect tracking."""
    
    page_number: str = Field(description="The source manga page number(s) or chapter segment.")
    prose_content: str = Field(description="The fully rendered R18 prose narrative in Vietnamese.")
    word_count: int = Field(description="The total word count of the generated prose.")
    metrics: LegacyMetrics = Field(description="Legacy mention counters kept for backward compatibility.")
    format_compliance: FormatCompliance = Field(description="Checks for correct markdown formatting and light-novel style rules.")
    sensory_affect: SensoryAffect = Field(description="Advanced visual, tactile, olfactory, dialogue, and tsundere metrics.")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page_number": "Page_14",
                "prose_content": "Reira thở dốc, hai má đỏ bừng nóng hổi...",
                "word_count": 450,
                "metrics": {
                    "smell_mentions": 3,
                    "sound_mentions": 3,
                    "texture_mentions": 5,
                    "temperature_mentions": 2
                },
                "format_compliance": {
                    "has_header": True,
                    "has_footer": True,
                    "valid_dialogue_format": True,
                    "valid_sfx_format": True
                },
                "sensory_affect": {
                    "olfactory": ["mùi tinh dịch tươi nồng", "hương cơ thể loli quyến rũ"],
                    "tactile": ["ma sát nóng ran", "chất nhờn nhớp nháp bôi khắp đùi"],
                    "visual": ["đùi run bần bật", "mắt trợn ngược vì sướng", "má ửng hồng"],
                    "dialogue_escalation": "TSUN-TSUN",
                    "tsundere_breakdown": 6.5,
                    "stroking_metric": 9
                }
            }
        }
    )
