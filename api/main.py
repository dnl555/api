import sys
import logging
from fastapi import FastAPI
from api.hello import router as hello_router
from api.auth_router import AuthRoute


# adds the app core to the import path
sys.path.insert(0, "..")

from app.core.logger import setup_logging, get_handler
from app.core.db import setup_db

description = """
This amazing API helps you do awesome stuff. 🚀
"""


app = FastAPI(
    title="Awesome API",
    description=description,
    version="0.0.1",
)


@app.on_event("startup")
async def startup_event():
    # custom log
    setup_logging()

    # uvicorn and fastapi log
    logging.getLogger("uvicorn.info").addHandler(get_handler())
    logging.getLogger("uvicorn.error").addHandler(get_handler())
    logging.getLogger("uvicorn.access").addHandler(get_handler())

    setup_db()


# api

router = AuthRoute()

# include hello router
router.include_router(hello_router)

app.include_router(router, prefix="/api", tags=["api_auth"])


@app.get("/")
async def root():
    return {"message": "Amazing API"}
