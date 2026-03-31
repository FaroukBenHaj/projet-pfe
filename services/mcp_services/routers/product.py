from pydantic import BaseModel 
from fastapi import APIRouter, Depends
from defectdojo.client import *
from defectdojo.schemas.product import Product

router = APIRouter(prefix="/products", tags=["Products"])
#TODO: implement product CRUD operations using client functions from tools/product.py
