from fastapi import FastAPI
from tools.productType import router as product_type_router

app = FastAPI(title="MCP Services")
app.include_router(product_type_router , prefix="/api/v2")

@app.get("/")
async def root():
    return {"message": "Welcome to MCP Services!"}