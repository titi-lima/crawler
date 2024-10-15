from fastapi import APIRouter, Depends
from infra.http.controllers.scraper import app
from infra.http.middlewares.auth import api_key_auth

router = APIRouter()

router.include_router(app, prefix="/scraper", tags=["scraper"], dependencies=[Depends(api_key_auth)])