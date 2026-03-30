from pydantic import BaseModel 
from fastapi import APIRouter, Depends
from defectdojo.client import *
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

@router.get("/product_types/")
async def tool_list_product_type():
    return await (get_product_type_list())

@router.get("/product_types/{id}/")
async def tool_get_product_type(id: int):
    return await (get_product_type(id))

@router.delete("/product_types/{id}/")
async def tool_delete_product_type(id: int):
    return await (delete_product_type(id))

@router.patch("/product_types/{id}/")
async def tool_update_product_type(id: int, request: ProductType):
    data = {
        "name": request.name,
        "description": request.description,
        "critical_product": request.critical_product,
        "key_product": request.key_product
    }
    return await (update_product_type(id, data))

@router.put("/product_types/{id}/")
async def tool_put_product_type(id: int, request: ProductType):
    data = {
        "name": request.name,
        "description": request.description,
        "critical_product": request.critical_product,
        "key_product": request.key_product
    }
    return await (full_update_product_type(id, data))