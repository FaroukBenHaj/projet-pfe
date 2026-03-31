from pydantic import BaseModel 
from fastapi import APIRouter, Depends
from client import *
from schemas.product import Product
from tools.product import *

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
async def tool_create_product(request: Product):
    response = await create_product(request)
    return response

@router.get("/")
async def tool_list_product():
    return await (get_product_list())

@router.get("/{id}/")
async def tool_get_product(id: int):
    return await (get_product(id))

@router.delete("/{id}/")
async def tool_delete_product(id: int):
    return await (delete_product(id))

@router.patch("/{id}/")
async def tool_update_product(id: int, request: Product):
    return await (update_product(id, request))

@router.put("/{id}/")
async def tool_put_product(id: int, request: Product):
    return await (full_update_product(id, request))

