from typing import Optional, Literal, Dict, Any, List
from pydantic import BaseModel, Field

class ScreenplayElement(BaseModel):
    """Represents a single flattened element of a Ren'Py script execution timeline."""
    type: Literal["dialogue", "scene", "show", "play_music", "play_sound", "play_movie", "stop_audio"] = Field(
        description="Type of the screenplay action"
    )
    # Dialogue fields
    speaker: Optional[str] = Field(default=None, description="Name or identifier of the character speaking")
    text: Optional[str] = Field(default=None, description="Substituted dialogue text spoken by the character")
    vpunch: Optional[bool] = Field(default=None, description="Whether visual punch effect (vpunch/hpunch) is active")
    
    # Scene/Show/Audio fields
    value: Optional[str] = Field(default=None, description="Value or identifier for bg, music, sound or movie")
    effects: Optional[str] = Field(default=None, description="Visual effects associated with scene/show changes")
    character: Optional[str] = Field(default=None, description="Name of character to show")
    expression: Optional[str] = Field(default=None, description="Details of character expression, clothes, pose")
    channel: Optional[str] = Field(default=None, description="Audio/video channel name for stop_audio")
    
    # Asset resolution fields
    asset_path: Optional[str] = Field(default=None, description="Physical path to referenced asset, if resolved under asset-root")
    desc: Optional[str] = Field(default=None, description="Human readable description of the action")

class ScreenplayMetadata(BaseModel):
    """Compilation metadata for a playthrough segment."""
    start_label: str = Field(description="Ren'Py start label name")
    total_elements: int = Field(description="Total elements in the compiled playthrough")
    variables: Dict[str, str] = Field(default_factory=dict, description="Final variable values substituted during compile")

class ScreenplayOutput(BaseModel):
    """Full schema for compiled playthrough novel screenplay outputs."""
    screenplay: List[ScreenplayElement] = Field(description="Sequence of screenplay elements")
    metadata: ScreenplayMetadata = Field(description="Compilation metadata")
