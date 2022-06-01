from django.test import TestCase
import requests

from rest_framework import status


class FileCSVTest(TestCase):
    def setUp(self):
        files = {'csvfile': open('postcodesgeo.csv', 'rb')}
        response = requests.post(
            'http://localhost:8000/api/filecsv/upload/postcodesgeo',
            files=files)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_upload_file(self):
        files = {'csvfile': open('postcodesgeo.csv', 'rb')}
        response = requests.post(
            'http://localhost:8000/api/filecsv/upload/postcodesgeo',
            files=files)

        assert response.status_code == status.HTTP_204_NO_CONTENT
