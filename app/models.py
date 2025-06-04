from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

class StoryNode(BaseModel):
    step: int
    text: str
    choices: List[str]
    decision: Optional[str] = None

class MichiStats(BaseModel):
    energy: int = 100
    reputation: str = "unknown"
    allies: List[str] = []

class MichiStory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    player_name: str
    current_step: int = 1
    story: List[StoryNode] = []
    stats: MichiStats = Field(default_factory=MichiStats)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)