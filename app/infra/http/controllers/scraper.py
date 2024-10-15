from application.services.scraper import ScraperService
from application.domain.scraper import Scraper
from fastapi import APIRouter

app = APIRouter()

class ScraperController:
    @staticmethod
    @app.post("/")
    def scrape(url: Scraper):
        return ScraperService.scrape(url)
