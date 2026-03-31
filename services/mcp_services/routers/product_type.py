from pydantic import BaseModel 
from fastapi import APIRouter, Depends
from client import *
from schemas.productType import ProductType
from tools.productType import *

router = APIRouter(prefix="/product_types", tags=["Product Types"])


@router.post("/")
async def tool_create_product_type(request: ProductType):
    response = await create_product_type(request)
    return response

@router.get("/")
async def tool_list_product_type():
    return await (get_product_type_list())

@router.get("/{id}/")
async def tool_get_product_type(id: int):
    return await (get_product_type(id))

@router.delete("/{id}/")
async def tool_delete_product_type(id: int):
    return await (delete_product_type(id))

@router.patch("/{id}/")
async def tool_update_product_type(id: int, request: ProductType):
    return await (update_product_type(id, request))

@router.put("/{id}/")
async def tool_put_product_type(id: int, request: ProductType):
    return await (full_update_product_type(id, request))

