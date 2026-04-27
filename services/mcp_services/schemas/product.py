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
    WEB_SERVICE = "web service"
    DESKTOP = "desktop"
    IOT = "iot"
    MOBILE = "mobile"
    WEB = "web"

class Lifecycle (str, Enum):
    CONSTRUCTION = "construction"
    PRODUCTION = "production"
    RETIREMENT = "retirement"

class Origin (str, Enum):
    THIRD_PARTY_LIBRARY = "third party library"
    PURCHASED = "purchased"
    CONTRACTOR = "contractor"
    INTERNAL = "internal"
    OPEN_SOURCE = "open source"

class Product(BaseModel):
    description: str
    name: str
    prod_type: int
    business_criticality: Optional[BusinessCriticality] = BusinessCriticality.NONE
    platform: Optional[Platform] = Platform.WEB_SERVICE
    lifecycle: Optional[Lifecycle]= Lifecycle.CONSTRUCTION
    origin: Optional[Origin]= Origin.INTERNAL
    tags: Optional[list[str]]=[]
    prod_numeric_grade: Optional[int] = None
    user_records: Optional[int] = None
    revenue: Optional[str]= None
    external_audience: Optional[bool] = False
    internet_accessible: Optional[bool] = False
    enable_product_tag_inheritance: Optional[bool] = False
    enable_simple_risk_acceptance: Optional[bool] = False
    enable_full_risk_acceptance: Optional[bool] = False
    disable_sla_breach_notifications: Optional[bool] = False
    # product_manager: Optional[int]
    # technical_contact: Optional[int]
    # team_manager: Optional[int]
    # sla_configuration: Optional[int]
    # regulations: Optional[list[int]] = None

class ProductUpdate(Product):
    name: Optional[str] = None
    prod_type: Optional[int] = None
    description: Optional[str] = None