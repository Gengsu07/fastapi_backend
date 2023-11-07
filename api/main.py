from fastapi import FastAPI

from api.routers.post import router as postRouter

app = FastAPI()


post_data = {}


app.include_router(postRouter)
