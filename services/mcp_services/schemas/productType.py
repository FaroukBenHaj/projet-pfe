from typing import Optional
from pydantic import BaseModel

class ProductType(BaseModel):
    name: str
    description: Optional[str] = None
    critical_product: Optional[bool] = False
    key_product: Optional[bool] = False

class ProductTypeUpdate(ProductType):
    name: Optional[str] = None

class ProductTypeResponse(ProductType):
    id: int