import time
import os
from pathlib import Path

from django.shortcuts import render
from django.conf import settings
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.core.files.storage import default_storage

from .producer import publish


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, filename, format=None):
        csvfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(csvfile.name + f"_{time.time()}.csv", csvfile)
        uploaded_file_url = fs.url(filename)

        publish("file_uploaded", {
            'filename': filename,
            'file_url': uploaded_file_url
        })

        return Response(status=204, data={
            'message': "The file has been uploaded correctly"
        })
