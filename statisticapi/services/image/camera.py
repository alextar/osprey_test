from utils.db import get_connection
from core import config


class DbService:

    def __init__(self):
        self.db = get_connection()


class CameraDbService(DbService):

    @property
    def cameras(self):
        return self.db[config.CAMERAS_COLLECTION].find(
            {}, {'_id': 0, 'camera_id': 1, 'timeout_error': 1, 'timeout': 1}
        ).sort('camera_id', -1)
