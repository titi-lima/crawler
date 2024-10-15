from pydantic import BaseModel

class Scraper(BaseModel):
    url: str