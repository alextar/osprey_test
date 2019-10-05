from core import config
from utils.db import get_connection
from random import randint, randrange


def _init_images():
    return [{'file_size': randrange(150, 55000, 1)} for i in range(randrange(20000, 100000, 100))]


def init_db(cameras_data=None):
    db = get_connection()
    db[config.CAMERAS_COLLECTION].drop()

    if cameras_data:
        for data in cameras_data:
            db[config.CAMERAS_COLLECTION].insert_one(data)
    else:
        generate_cameras()

    db.cameras.create_index('camera_id')


def generate_cameras():
    db = get_connection()
    timeout_error = config.CAMERAS_REQUEST_TIMEOUT_ERROR
    for camera_id in range(config.CAMERAS_COUNT):
        camera_data = {
            'camera_id': camera_id,
            'timeout_error': timeout_error > 0,
            'timeout': randint(30, 40),
            'images': _init_images()
        }

        timeout_error -= 1
        db[config.CAMERAS_COLLECTION].insert_one(camera_data)





