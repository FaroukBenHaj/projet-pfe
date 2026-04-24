from pydantic import BaseModel 
from typing import Optional

class TestType(BaseModel):
    name: str 
    static_tool: Optional[bool] = False
    dynamic_tool: Optional[bool] = False
    active: Optional[bool] = True

class TestTypeUpdate(TestType):
    name: Optional[str] = None