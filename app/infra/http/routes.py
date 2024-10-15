from fastapi import APIRouter, Depends
from infra.http.middlewares.auth import api_key_auth
from infra.http.controllers.scraper import app as scraper_app
from infra.http.controllers.receipts import app as receipts_app

router = APIRouter()

router.include_router(scraper_app, prefix="/scraper", tags=["scraper"], dependencies=[Depends(api_key_auth)])
router.include_router(receipts_app, prefix="/receipts", tags=["receipts"], dependencies=[Depends(api_key_auth)])