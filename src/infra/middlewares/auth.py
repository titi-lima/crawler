#api key authentication
import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def api_key_auth(api_key: str = Security(api_key_header)):
    expected_api_key = os.getenv("API_KEY")
    if api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Incorrect API key provided")
    return api_key
