from fastapi import FastAPI

from services.image.statistic import CameraService


app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "Hello World"}


@app.get("/statistic")
async def statistic():
    return CameraService().aggregated_data

