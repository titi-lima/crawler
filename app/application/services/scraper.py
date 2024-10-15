import requests
from bs4 import BeautifulSoup
from fastapi.exceptions import HTTPException

class ScraperService:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, features='xml')

            receipt_id = soup.find('nNF').text
            receipt_date = soup.find('dhEmi').text
            receipt_price = soup.find('vNF').text

            products = []

            for prod in soup.find_all('prod'):
                id = prod.find('cProd').text
                name = prod.find('xProd').text
                price = prod.find('vProd').text
                products.append({"id": id, "name": name, "price": price})
            
            data = {
                "id": receipt_id,
                "date": receipt_date,
                "price": receipt_price,
                "products": products
            }

            return {"message": "Page scraped successfully", "data": data}
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"HTTP Error: {e}")
        except requests.exceptions.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            raise HTTPException(status_code=500, detail=f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            raise HTTPException(status_code=504, detail=f"Timeout Error: {e}")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Request Error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")