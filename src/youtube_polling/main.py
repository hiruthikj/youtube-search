import logging
from contextlib import asynccontextmanager

from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .common.constants import RequestStatus
from .config import settings
from .database import SessionLocal
from .extenstions.logger_setup import setup_logging
from .extenstions.middleware import RequestContextLogMiddleware
from .logic import fetch_from_yt
from .route import search_router

# from .logic import fetch_from_yt


setup_logging(debug=settings.DEBUG)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.DEBUG and logging.warning(f"DEBUG={settings.DEBUG}")
    logging.debug("Setting Up App...")

    try:
        # TODO
        pass
    except Exception:
        logging.critical("Could not connect to DB", exc_info=True)
        exit(1)


    async with AsyncScheduler() as scheduler:
        app.state.scheduler = scheduler

        try:
            await app.state.scheduler.add_schedule(
                func_or_task_id=fetch_from_yt,
                trigger=IntervalTrigger(seconds=settings.POLL_INTERVAL_SECONDS),
                # next_run_time=datetime.now(tz=timezone.utc),
            )
            # await app.state.scheduler.wait_until_stopped()

            await app.state.scheduler.run_until_stopped()
        except Exception:
            logging.critical("CRON Scheduling failed", exc_info=True)
            await app.state.scheduler.stop()

    yield

    # on shutdown
    logging.info("Cleaning up...")
    logging.info("Shutting down CRON...")
    # await app.state.scheduler.stop()

    logging.shutdown()
    logging.info("Cleaning done")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    lifespan=lifespan
)
app.add_middleware(RequestContextLogMiddleware)

app.include_router(router=search_router)


@app.get("/healthcheck")
async def healthcheck():
    return await fetch_from_yt()
    return "OK"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_response = {
        "status": RequestStatus.FAIL,
        "error": {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Request Validation Failed",
            "errors": exc.errors(),
        },
    }
    return JSONResponse(
        content=jsonable_encoder(error_response),
        status_code=status.HTTP_400_BAD_REQUEST,
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
