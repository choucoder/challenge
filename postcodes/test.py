import pytest
import requests

from decouple import config


def test_postcodes_api_request_correct():
    url = f'https://api.postcodes.io/postcodes?lon=-1.474217&lat=52.923454'
    response = requests.get(url)
    assert response.status_code == 200 and response.json()['result']


def test_postcodes_api_request_wrong():
    url = f'https://api.postcodes.io/postcodes?lon=-0&lat=0'
    response = requests.get(url)
    assert response.status_code == 200 and response.json()['result'] == None


def test_save_postcode():
    lat = 52.923454
    lon = -1.474217

    url = f'https://api.postcodes.io/postcodes?lon={lon}&lat={lat}'
    response = requests.get(url)
    response = response.json()
    postcode = response['result'][0]['postcode']

    data = {
        'lat': 52.923454,
        'lon': -1.474217,
        'code': postcode,
    }
    print("host=", config("host"))
    response = requests.post(
        f'http://{config("host")}:8000/api/postcodes', json=data)

    assert response.status_code == 201
