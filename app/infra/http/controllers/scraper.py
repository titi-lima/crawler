from application.services.scraper import ScraperService
from application.domain.scraper import Scraper
from fastapi import APIRouter

app = APIRouter()

class ScraperController:
    @staticmethod
    @app.post("/", status_code=201)
    def scrape(scraper: Scraper):
        scraper_service = ScraperService(scraper.url)
        data = scraper_service.scrape()
        return {"message": "Page scraped successfully", "data": data}
