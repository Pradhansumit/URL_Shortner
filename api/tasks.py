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


@shared_task
def update_click_counts():
    """Periodically updates database with click counts from Redis"""

    from django.db import transaction
    from django.db.models import F
    from django.core.cache import cache
    from django.utils.dateparse import parse_datetime

    keys = cache.keys("click_count:*")  # Get all click count keys
    print(f"Found Redis keys: {keys}")  # Log keys for debugging

    with transaction.atomic():
        for key in keys:
            short_url = key.split(":")[-1]
            count = cache.get(key)
            last_visited_key = f"last_visited:{short_url}"
            last_visited_str = cache.get(last_visited_key)
            print(
                f"Processing {short_url} | Clicks: {count} | Last Visited: {last_visited_str}"
            )

            if count:
                update_data = {"click_count": F("click_count") + count}

                if last_visited_str:
                    last_visited = parse_datetime(last_visited_str)
                    update_data["last_clicked"] = last_visited

                rows_updated = ShortURL.objects.filter(
                    hash_code__istartswith=short_url
                ).update(**update_data)
                print(f"Updated {rows_updated} row(s) in DB for {short_url}")
                cache.delete(key)  # Clear cached count after updating DB
                cache.delete(last_visited_key)  # Clear last visited timestamp
