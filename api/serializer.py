from rest_framework import serializers
from api.models import ShortURL


class ShortURL_Serializer(serializers.Serializer):
    original_url = serializers.URLField(required=True)
