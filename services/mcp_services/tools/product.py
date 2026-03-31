from schemas.product import Product as ProductSchema
from client import request


#Product CRUD :
async def create_product(data: ProductSchema):
        return await request("POST", "products/", json=data.dict()) 

async def get_product_list():
        return await request("GET", "products/") 

async def get_product(id: int):
        return await request("GET", f"products/{id}/") 

async def delete_product(id: int):
        return await request("DELETE", f"products/{id}/") 

async def update_product(id: int, data: ProductSchema):
        return await request("PATCH", f"products/{id}/", json=data.model_dump(exclude_none=True)) 

async def full_update_product(id: int, data: ProductSchema):
        return await request("PUT", f"products/{id}/", json=data.model_dump(exclude_none=True)) 
