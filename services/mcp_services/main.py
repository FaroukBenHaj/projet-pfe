from fastapi import FastAPI
from routers.product_type import router as product_type_router
from routers.product import router as product_router

app = FastAPI(title="MCP Services")
app.include_router(product_type_router )
app.include_router(product_router )
@app.get("/")
async def root():
    return {"message": "Welcome to MCP Services!"}