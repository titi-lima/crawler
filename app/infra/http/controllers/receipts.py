from application.services.receipt import ReceiptService
from application.domain.receipt import Receipt
from fastapi import APIRouter, Response

app = APIRouter()

class ReceiptController:
    @staticmethod
    @app.get("/")
    def get_all_receipts(response: Response):
        receipt_service = ReceiptService()
        receipts = receipt_service.get_all()

        if len(receipts) == 0:
            response.status_code = 204
            return {"message": "No receipts found"}

        return {"message": "Receipts found", "data": receipts}

    @staticmethod
    @app.get("/{receipt_id}")
    def get_receipt(receipt_id: str):
        receipt_service = ReceiptService()
        receipt = receipt_service.get(receipt_id)
        return {"message": "Receipt found", "data": receipt}
    
        return receipt_service.get(receipt_id)