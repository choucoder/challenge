from rest_framework import serializers
from .models import Postcode


class PostcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postcode
        fields = '__all__'
