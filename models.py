from pydantic import BaseModel
from typing import List, Optional

class Suspect(BaseModel):
    suspect_id: int
    name: str
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    eye_color: Optional[str] = None
    hair_color: Optional[str] = None
    last_known_location: Optional[str] = None
    
class CallInfo(BaseModel):
    caller_name: str
    location: str
    urgency: Optional[str] = None
    description: Optional[str] = None
    suspects: List[Suspect] = []