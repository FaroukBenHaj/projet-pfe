# Fix — register tools before running
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from tools import ( 
    products_type_tools ,
    products_tools,
    engagements_tools,
    test_tools,
    test_types_tools,
    findings_tools
    ) 
load_dotenv()
from tools.products_type_tools import router as products_type_router
from tools.products_tools import router as products_router
from tools.engagements_tools import router as engagements_router
from tools.test_tools import router as test_router
from tools.test_types_tools import router as test_types_router
from tools.findings_tools import router as findings_router

from fastapi import APIRouter

router = APIRouter()
app = FastAPI()
app.include_router(products_type_router, tags=["products-types"])
# products_type_tools.register_tools(app)
app.include_router(products_router, tags=["products"])
# products_tools.register_tools(app)
app.include_router(engagements_router, tags=["engagements"])
# engagements_tools.register_tools(app)
app.include_router(test_router, tags=["tests"])
# test_tools.register_tools(app)
app.include_router(test_types_router, tags=["test-types"])
# test_types_tools.register_tools(app)
app.include_router(findings_router, tags=["findings"])
# findings_tools.register_tools(app)

if __name__ == "__main__":
     uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8081,
        reload=True
    )
