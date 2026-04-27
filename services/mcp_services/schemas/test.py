from typing import Optional
from pydantic import BaseModel
from datetime import datetime , date

class Test(BaseModel):
    engagement: int
    test_type: int 
    target_start: datetime
    target_end: datetime
    notes: Optional[list[int]] = None
    tags: Optional[list[str]] = None
    scan_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    percent_complete: Optional[int] = None
    version: Optional[str] = None
    build_id: Optional[str] = None
    commit_hash: Optional[str] = None
    branch_tag: Optional[str] = None
    lead: Optional[int] = None
    environment: Optional[int] = None
    api_scan_configuration: Optional[int] = None

class TestUpdate(Test):
    test_type: Optional[int] = None
    target_start: Optional[datetime] = None
    target_end: Optional[datetime] = None
    engagement: Optional[int] = None