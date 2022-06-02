import time
import os

from django.conf import settings
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage

from .producer import publish


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, filename, format=None):
        csvfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(csvfile.name + f"_{time.time()}.csv", csvfile)
        uploaded_file_url = fs.url(filename)

        fcsv = open(os.path.join(settings.MEDIA_ROOT, filename))
        content = fcsv.read()

        if 'lat,lon\n' in content:
            publish("file_uploaded", {
                'filename': filename,
                'file_url': uploaded_file_url
            })

            return Response(status=status.HTTP_204_NO_CONTENT, data={
                'message': "The file has been uploaded correctly"
            })
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'message': "The File has errors"
            })
