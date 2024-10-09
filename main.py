from fastapi import Depends, FastAPI
from src.infra.middlewares.auth import api_key_auth

app = FastAPI(dependencies=[Depends(api_key_auth)])

@app.get("/")
def health_check():
    return {"message": "Made with ❤️ by titi-lima 🇧🇷"}
