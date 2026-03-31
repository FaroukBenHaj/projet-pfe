from typing import Optional
from pydantic import BaseModel

class ProductType(BaseModel):
    name: str
    description: Optional[str]=""
    critical_product: Optional[bool]=True
    key_product: Optional[bool]=True
