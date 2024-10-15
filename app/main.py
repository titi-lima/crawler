from fastapi import FastAPI
from infra.http.middlewares import error_handler
from infra.http.middlewares.auth import api_key_auth
from mangum import Mangum
from infra.http.routes import router

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Made with ❤️ by titi-lima 🇧🇷"}

app.include_router(router)

app.add_exception_handler(Exception, error_handler)

handler = Mangum(app)