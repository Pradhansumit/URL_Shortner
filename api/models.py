import uuid
from django.db import models


class ShortURL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_url = models.CharField(unique=True)
    hash_code = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)
    last_clicked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.short_code


class URL_Logs(models.Model):
    url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name="url_info")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.CharField(blank=True, null=True)
    # country = models.charfield(max_length=50, blank=True, null=True) # not solve how to get the geo location with third party api
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url + " " + self.user_agent
