from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import PostcodeSerializer
from .models import Postcode


class PostcodeAPIView(APIView):

    def post(self, request):
        data = request.data
        serializer = PostcodeSerializer(data=data)

        if serializer.is_valid():
            postcode = serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=serializer.data
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
