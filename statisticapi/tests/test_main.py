import json

from starlette.testclient import TestClient
from deepdiff import DeepDiff

from tests.utils.db import init_db
from main import app

client = TestClient(app)

cameras_data = [
    {'camera_id': 1, 'timeout_error': True, 'timeout': 1, 'images': [{'file_size': 100}]},
    {'camera_id': 2, 'timeout_error': False, 'timeout': 5, 'images': [
        {'file_size': 100}, {'file_size': 100}, {'file_size': 400}
    ]},
    {'camera_id': 3, 'timeout_error': False, 'timeout': 5, 'images': [{'file_size': 200}, {'file_size': 400}]}
]


# def test_big_dataset():
#     """
#     Chack that if works with big dataset
#     Check timeout
#     """
#     init_db()
#     response = client.get("/statistic")
#     assert response.status_code == 200
#     data = response.json()
#
#     assert len(data['cameras']) == config.CAMERAS_COUNT - config.CAMERAS_REQUEST_TIMEOUT_ERROR


def test_calculation():
    """
    Check statistic calculation
    Check timeout
    """
    init_db(cameras_data)
    response = client.get("/statistic")
    assert response.status_code == 200
    data = response.json()

    assert not DeepDiff(data, {
        'cameras': [
            {'camera_id': 2, 'image_count': 3, 'max_file_size': 400, 'total_file_size': 600},
            {'camera_id': 3, 'image_count': 2, 'max_file_size': 400, 'total_file_size': 600}
        ],
        'statistics': {
            'max_data_usage': [{'camera_id': 2, 'value': 600}, {'camera_id': 3, 'value': 600}],
            'max_image_count': [{'camera_id': 2, 'value': 3}],
            'max_image_size': [{'camera_id': 2, 'value': 400}, {'camera_id': 3, 'value': 400}]
        }
    }, ignore_order=True)

