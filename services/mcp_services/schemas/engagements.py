from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date


class EngagementStatus(str, Enum):
    NOT_STARTED = "Not Started"
    BLOCKED = "Blocked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    SCHEDULED = "Scheduled"
    WAITING_FOR_RESOURCE = "Waiting for Resource"


class EngagementType(str, Enum):
    INTERACTIVE = "Interactive"
    CICD = "CI/CD"


class Engagement(BaseModel):
    product: int  
    target_start: date
    target_end: date
    tag: Optional[list[str]] = []
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    first_contacted: Optional[date] = None
    reason: Optional[str] = None
    tracker: Optional[str] = None
    test_strategy: Optional[str] = None
    threat_model: bool = False
    api_test: bool = False
    pen_test: bool = False
    check_list: bool = False
    status: EngagementStatus = EngagementStatus.NOT_STARTED
    engagement_type: EngagementType = EngagementType.INTERACTIVE
    build_id: Optional[str] = None
    commit_hash: Optional[str] = None
    branch_tag: Optional[str] = None
    source_code_management_uri: Optional[str] = None
    deduplication_on_engagement: bool = False
    lead: Optional[int] = None
    requester: Optional[int] = None
    preset: Optional[int] = None
    report_type: Optional[int] = None
    build_server: Optional[int] = None
    source_code_management_server: Optional[int] = None
    orchestration_engine: Optional[int] = None

class EngagementUpdate(Engagement):
    target_start: Optional[date] = None
    target_end: Optional[date] = None
    name: Optional[str] = None
