from infra.data_access.dynamodb_client import get_dynamodb_client
from application.domain.receipt import Receipt

class ReceiptRepository:
    def __init__(self, table_name: str):
        self.client = get_dynamodb_client()
        self.table = self.client.Table(table_name)
    
    def create(self, receipt: Receipt):
        self.table.put_item(Item=receipt)
    
    def get(self, receipt_id: str):
        response = self.table.get_item(Key={"receipt_id": receipt_id})
        return response.get("Item")