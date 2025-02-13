from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from api.services import (
    add_url_information,
    generate_short_url,
    get_original_url,
    get_url_information_from_request,
)
from api.serializer import ShortURL_Serializer


class Create_hash_short_url(APIView):
    def post(self, request, format=None):
        serializer = ShortURL_Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        original_url = serializer.validated_data["original_url"]
        if not original_url:
            return Response(
                {"error": "Please provide original url."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        get_short_url = generate_short_url(original_url=original_url)
        return Response({"short_url": get_short_url}, status=status.HTTP_200_OK)


class Redirect_to_original_url(APIView):
    def get(self, request, url):
        print(url)
        original_url = get_original_url(short_url=url)
        if original_url is None:
            return Response(
                {"error": "Invalid URL."}, status=status.HTTP_400_BAD_REQUEST
            )

        get_url_information_from_request(request, original_url)

        return redirect(original_url)
