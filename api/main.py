import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers.post import router as postRouter

os.environ["ENV_STATE"] = "test"
from api.database import database  # noqa:E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(postRouter)
