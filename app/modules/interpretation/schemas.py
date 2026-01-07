from typing import Dict, Optional, Any
from pydantic import BaseModel, Field

class InterpretationContext(BaseModel):
    prompt: str
    user_groups: Dict[str, str] = Field(default_factory=dict) # ID -> Name
    user_goals: Dict[str, str] = Field(default_factory=dict)  # ID -> Name (New!)

class InterpretationData(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    frequency: Optional[str] = None
    day_of_week: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    conditions: Optional[str] = None
    
    # Matching Results
    is_existing_group: bool = False
    group_name: Optional[str] = None
    group_id: Optional[str] = None
    
    is_existing_goal: bool = False
    goal_name: Optional[str] = None
    goal_id: Optional[str] = None

class InterpretationResult(BaseModel):
    intent: str # "group_saving" or "individual_saving" or "personal_saving"
    data: InterpretationData
    raw_prompt: str
