from pydantic import BaseModel 
from fastapi import APIRouter, Depends
from defectdojo.client import create_product_type
from typing import Optional

router = APIRouter()

class ProductType(BaseModel):
    name: str
    description: Optional[str]=""
    critical_product: Optional[bool]=True
    key_product: Optional[bool]=True

@router.post("/product_types/")
async def tool_create_product_type(request: ProductType):
    response = await create_product_type(
        name=request.name,
        description=request.description,
        critical_product=request.critical_product,
        key_product=request.key_product
    )
    return response