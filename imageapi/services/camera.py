from utils.db import get_connection
from core import config
import time

class DbService:

    def __init__(self):
        self.db = get_connection()


class CameraService(DbService):

    def get_camera(self, camera_id):
        camera = self.db[config.CAMERAS_COLLECTION].find_one({'camera_id': int(camera_id)}, {'_id': 0})

        if camera['timeout_error']:
            time.sleep(int(camera['timeout']) + 5)

        return camera
