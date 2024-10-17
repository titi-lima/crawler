import unittest
from unittest.mock import MagicMock, patch
from application.services.receipt import ReceiptService
from fastapi.exceptions import HTTPException

class TestReceiptService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.patcher = patch('application.services.receipt.ReceiptRepository', return_value=self.mock_repo)
        self.patcher.start()
        
        self.service = ReceiptService()
    
    def tearDown(self):
        self.patcher.stop()
    
    def test_get_all(self):
        self.mock_repo.get_all.return_value = ["receipt1", "receipt2"]
        
        result = self.service.get_all()
        self.assertEqual(result, ["receipt1", "receipt2"])
        self.mock_repo.get_all.assert_called_once()
    
    def test_get_existing_receipt(self):
        self.mock_repo.get.return_value = {"id": "1", "date": "2022-01-01"}
        
        receipt = self.service.get("1")
        self.assertIsNone(receipt)
        self.mock_repo.get.assert_called_once_with("1")
    
    def test_get_nonexistent_receipt(self):
        self.mock_repo.get.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            self.service.get("nonexistent_id")
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Receipt not found")
    
    def test_delete_existing_receipt(self):
        self.mock_repo.get.return_value = {"id": "1", "date": "2022-01-01"}
        self.mock_repo.delete.return_value = True
        
        result = self.service.delete("1")
        self.assertTrue(result)
        self.mock_repo.get.assert_called_once_with("1")
        self.mock_repo.delete.assert_called_once_with("1", "2022-01-01")
    
    def test_delete_nonexistent_receipt(self):
        self.mock_repo.get.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            self.service.delete("nonexistent_id")
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Receipt not found")

if __name__ == '__main__':
    unittest.main()