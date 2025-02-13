from django.urls import path
from api.views import Create_hash_short_url, Redirect_to_original_url

urlpatterns = [
    path("shortner/", Create_hash_short_url.as_view(), name="create-hash-sort-url"),
    path(
        "<str:url>/",
        Redirect_to_original_url.as_view(),
        name="redirect-to-original-url",
    ),
]
