# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class AgentStep(BaseModel):
    description: str

class AgentResponse(BaseModel):
    agent: str
    query: str
    steps: List[AgentStep]
    response: Optional[str] = None
    visual: Optional[str] = None
    follow_up: Optional[str] = None

class QueryRequest(BaseModel):
    user_query: str
