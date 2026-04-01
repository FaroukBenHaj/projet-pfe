from schemas.productType import ProductType as ProductTypeSchema
from client import request


#Product types CRUD :
async def create_product_type(data: ProductTypeSchema):
        return await request("POST", "product_types/", json=data.dict()) 

async def get_product_type_list():
        return await request("GET", "product_types/") 

async def get_product_type(id: int):
        return await request("GET", f"product_types/{id}/") 

async def delete_product_type(id: int):
        return await request("DELETE", f"product_types/{id}/") 

async def update_product_type(id: int, data: ProductTypeSchema) -> dict :
        return await request("PATCH", f"product_types/{id}/", json=data.model_dump(exclude_none=True)) 

async def full_update_product_type(id: int, data: ProductTypeSchema):
        return await request("PUT", f"product_types/{id}/", json=data.model_dump(exclude_none=True)) 
