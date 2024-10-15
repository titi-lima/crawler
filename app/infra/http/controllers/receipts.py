from application.services.receipt import ReceiptService
from application.domain.receipt import Receipt
from fastapi import APIRouter

app = APIRouter()

class ReceiptController:
    @staticmethod
    @app.get("/")
    def get_all_receipts():
        receipt_service = ReceiptService()
        return receipt_service.get_all()

    @staticmethod
    @app.get("/{receipt_id}")
    def get_receipt(receipt_id: str):
        receipt_service = ReceiptService()
        return receipt_service.get(receipt_id)