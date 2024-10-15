from pydantic import BaseModel
from application.domain.products import Product

class Receipt(BaseModel):
    id: str
    date: str
    total: float
    products: list[Product]