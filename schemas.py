from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    name: str
    price: float


class ProductList(BaseModel):
    data: List[Product]
