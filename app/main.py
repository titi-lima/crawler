from fastapi import Depends, FastAPI
from infra.middlewares.auth import api_key_auth
from mangum import Mangum

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Made with ❤️ by titi-lima 🇧🇷"}

@app.get("/protected-path", dependencies=[Depends(api_key_auth)])
def protected_route():
    return {"message": "This route requires authentication"}

handler = Mangum(app)