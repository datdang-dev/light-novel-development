from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class BackgroundAsset(BaseModel):
    """Details of an indexed background asset."""
    path: str = Field(description="Relative path to bg image")
    description: str = Field(default="PENDING_ANALYSIS", description="Visual description of the background")
    atmosphere: str = Field(default="unknown", description="Atmosphere description")

class SpriteAsset(BaseModel):
    """Details of an indexed character sprite asset."""
    path: str = Field(description="Relative path to sprite image")
    character: str = Field(description="Character name")
    expression: str = Field(default="neutral", description="Expression/pose key")
    description: str = Field(default="PENDING_ANALYSIS", description="Visual description of the character sprite")

class VisualManifestOutput(BaseModel):
    """Full schema for visual assets manifest indexing."""
    backgrounds: Dict[str, BackgroundAsset] = Field(default_factory=dict, description="Indexed backgrounds")
    sprites: Dict[str, SpriteAsset] = Field(default_factory=dict, description="Indexed sprites")
    others: List[str] = Field(default_factory=list, description="Other media files")
