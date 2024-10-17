from infra.data_access.dynamodb_client import get_dynamodb_client
from application.domain.receipt import Receipt
from boto3.dynamodb.conditions import Key

class ReceiptRepository:
    def __init__(self, table_name: str):
        self.client = get_dynamodb_client()
        self.table = self.client.Table(table_name)
    
    def create(self, receipt: Receipt):
        self.table.put_item(Item=receipt)
    
    def get(self, receipt_id: str):
        response = self.table.query(
            KeyConditionExpression=Key("id").eq(receipt_id)
        )
        items = response.get("Items")
        return items[0] if items else None

    def get_all(self):
        response = self.table.scan()
        return response.get("Items")
    
    def delete(self, receipt_id: str, date: str):
        self.table.delete_item(Key={"id": receipt_id, "date": date})