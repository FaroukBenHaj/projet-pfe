
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class BusinessCriticality(str, Enum):
    VERY_HIGH = "very high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very low"
    NONE = "none"

class Platform(str, Enum):
    WEB_SERVICE = "web_service"
    DESKTOP = "desktop"
    IOT = "iot"
    MOBILE = "mobile"
    WEB = "web"

class Lifecycle (str, Enum):
    CONSTRUCTION = "Construction"
    PRODUCTION = "Production"
    RETIREMENT = "Retirement"

class Origin (str, Enum):
    THIRD_PARTY_LIBRARY = "Third Party Library"
    PURCHASED = "Purchased"
    CONTRACTOR = "Contractor Developed"
    INTERNAL = "Internally Developed"
    OPEN_SOURCE = "Open Source"
    OUTSOURCED = "Outsourced"

class Product(BaseModel):
    description: str
    name: str
    prod_type: int
    prod_type: int
    business_criticality: Optional[BusinessCriticality]
    platform: Optional[Platform]
    lifecycle: Optional[Lifecycle]
    origin: Optional[Origin]
    tags: Optional[list[str]]
    prod_numeric_grade: Optional[int]
    user_records: Optional[int]
    revenue: Optional[str]
    external_audience: Optional[bool]
    internet_accessible: Optional[bool]
    enable_product_tag_inheritance: Optional[bool]
    enable_simple_risk_acceptance: Optional[bool]
    enable_full_risk_acceptance: Optional[bool]
    disable_sla_breach_notifications: Optional[bool]
    product_manager: Optional[int]
    technical_contact: Optional[int]
    team_manager: Optional[int]
    sla_configuration: Optional[int]
    regulations: Optional[list[int]]

