import time
from fastapi import Depends, FastAPI
from random import randrange
from services.camera import CameraService


app = FastAPI()


@app.get("/")
async def root():
    return {'images': [{'len': randrange(150, 5000, 50)} for i in range(1000000)]}


@app.get("/camera/{camera_id}")
async def read_camera(camera_id):
    start = time.time()
    camera = CameraService().get_camera(camera_id)
    timeout = int(camera['timeout'])
    # dt = (time.time() - start) + 10

    # if timeout > dt:
    #     time.sleep(int(timeout - dt))

    return camera
