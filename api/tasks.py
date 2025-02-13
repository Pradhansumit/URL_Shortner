from datetime import timedelta
from celery import shared_task
from django.utils.timezone import now

from api.models import ShortURL, URL_Logs


@shared_task(name="delete_expired_urls")
def delete_expired_urls():
    """
    Deletes all the urls that has been created 7 days ago.
    """
    expiry_time = now() - timedelta(days=7)
    ShortURL.objects.filter(created_at__lt=expiry_time).delete()


@shared_task
def add_url_information(original_url, ip_address, user_agent, referrer):
    """
    Create a database entry about information regarding short url click.
    """
    url_obj = ShortURL.objects.filter(original_url=original_url).first()
    URL_Logs.objects.create(
        url=url_obj,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
    )
