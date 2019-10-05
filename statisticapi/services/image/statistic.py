from functools import reduce
import time
import concurrent.futures
import requests
from requests.exceptions import HTTPError

from services.image.camera import CameraDbService

CAMERA_API_URL = 'http://imageapi/'
from core.config import CAMERAS_COUNT
from services.image.camera import CameraDbService
CAMERAS = [i for i in range(CAMERAS_COUNT)]


class CameraService:

    def __init__(self):
        self.statistic_data = {
            'cameras': [],
            'statistics': {
                'max_data_usage': [],
                'max_image_count': [],
                'max_image_size': []
            }
        }

    def load_data_by_camera(self, camera, timeout):
        print(f'initate loading data for {camera}')

        try:
            response = requests.get(f'{CAMERA_API_URL}camera/{camera}', timeout=timeout)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:

            data = response.json()

            total_file_size = 0
            image_count = len(data["images"])
            max_file_size = 0
            for image in data['images']:
                total_file_size += image['file_size']
                if image['file_size'] > max_file_size:
                    max_file_size = image['file_size']

            return {
                'camera_id': camera,
                'total_file_size': total_file_size,
                'max_file_size': max_file_size,
                'image_count': image_count
            }

    @property
    def aggregated_data(self):

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # Start the load operations and mark each future with its URL
            future_to_camera = {
                executor.submit(
                    self.load_data_by_camera, camera['camera_id'], camera['timeout']
                ): camera['camera_id'] for camera in CameraDbService().cameras
            }

            for future in concurrent.futures.as_completed(future_to_camera):
                camera = future_to_camera[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (camera, exc))
                else:
                    if data:
                        self.statistic_data['cameras'].append(data)
                        self.prepare_stat_param(data, 'image_count', 'max_image_count')
                        self.prepare_stat_param(data, 'max_file_size', 'max_image_size')
                        self.prepare_stat_param(data, 'total_file_size', 'max_data_usage')

        return self.statistic_data

    def prepare_stat_param(self, camera, camera_key, stat_key):

        if len(self.statistic_data['statistics'][stat_key]):
            max_image_count = self.statistic_data['statistics'][stat_key][0]['value']
            if max_image_count < camera[camera_key]:
                self.statistic_data['statistics'][stat_key] = [
                    {'camera_id': camera['camera_id'], 'value': camera[camera_key]}
                ]
            elif max_image_count == camera[camera_key]:
                self.statistic_data['statistics'][stat_key].append(
                    {'camera_id': camera['camera_id'], 'value': camera[camera_key]}
                )
        else:
            self.statistic_data['statistics'][stat_key].append(
                {'camera_id': camera['camera_id'], 'value': camera[camera_key]}
            )

