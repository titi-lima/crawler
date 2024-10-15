from fastapi import HTTPException
from fastapi.responses import JSONResponse

def error_handler(_, exc):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )
    return JSONResponse(
        status_code=500,
        # Watch out here - this might be a security issue if we're ever integrating external APIs
        # as it might expose back an access token.
        content={"message": "Internal Server Error", "details": str(exc)},
    )