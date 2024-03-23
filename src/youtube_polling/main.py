from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .common.constants import RequestStatus
from .config import settings
from .extenstions.logger_setup import setup_logging
from .extenstions.middleware import RequestContextLogMiddleware

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
)
app.add_middleware(RequestContextLogMiddleware)


@app.get("/healthcheck")
async def healthcheck():
    return "OK"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_response = {
        "status": RequestStatus.FAIL,
        "error": {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Request Validation Failed",
            "errors": exc.errors(),
        },
    }
    return JSONResponse(
        content=jsonable_encoder(error_response),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error_response = {
        "status": RequestStatus.FAIL,
        "error": {
            "code": exc.status_code,
            "message": exc.detail,
            "errors": [],
        },
    }
    return JSONResponse(
        content=jsonable_encoder(error_response),
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: RequestValidationError):
    error_response = {
        "status": RequestStatus.FAIL,
        "error": {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error",
            "errors": [],
        },
    }
    return JSONResponse(
        content=jsonable_encoder(error_response),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# import uvicorn
# if __name__=="__main__":
#     uvicorn.run("app.main:app",host='0.0.0.0', port=8089)
