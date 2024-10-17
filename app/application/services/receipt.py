from fastapi.exceptions import HTTPException
from infra.data_access.receipt import ReceiptRepository

class ReceiptService:
    def __init__(self):
        self.receiptRepository = ReceiptRepository("receipts")

    def get_all(self):
        return self.receiptRepository.get_all()

    def get(self, receipt_id: str):
        receipt = self.receiptRepository.get(receipt_id)

        if receipt is None:
            raise HTTPException(status_code=404, detail="Receipt not found")
    
        return self.receiptRepository.get(receipt_id)