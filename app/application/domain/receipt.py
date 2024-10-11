from pydantic import BaseModel
from application.domain.products import Product

class Receipt(BaseModel):
    id: int
    products: list[Product]
    total: float
    payment_method: str
    access_key: str