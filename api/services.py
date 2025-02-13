import hashlib
import base64
from django.conf import settings
from api.models import ShortURL, URL_Logs
import datetime

from api.tasks import add_url_information


def generate_hash_code(original_url):
    """Generate a short code using SHA252 and base64 encoding."""

    # check if the original URL is already present in database.
    existing_entry = ShortURL.objects.filter(original_url=original_url).first()

    if existing_entry:
        return existing_entry.hash_code

    hash_object = hashlib.sha256(original_url.encode())  # create hash object
    hash_digest = hash_object.digest()  # returns hash object in binary format
    base64_decoded = base64.urlsafe_b64encode(
        hash_digest
    ).decode()  # returns base64 format of the binary format code, store it in the database

    ShortURL.objects.create(original_url=original_url, hash_code=base64_decoded)

    return base64_decoded


def generate_short_url(original_url):
    """Create shortened url from the original url"""

    base64_decoded = generate_hash_code(
        original_url=original_url
    )  # calls the function to generate hash code and store base64 format of hash code in the database
    shortened_url = f"{settings.BASE_DOMAIN}/api/{base64_decoded[:7]}"  # truncate the base64 to first 7 characters
    return shortened_url


def get_original_url(short_url):
    """Returns the original url from the base64 (hash) code that is with the url"""

    shortURLobj = ShortURL.objects.filter(hash_code__istartswith=short_url).first()
    if not shortURLobj:
        return None
    # adds last clicked everytime user clicks the link
    shortURLobj.last_clicked = datetime.datetime.now()
    shortURLobj.click_count += 1
    shortURLobj.save()

    original_url = shortURLobj.original_url
    return original_url


def get_url_information_from_request(request, original_url):
    """
    Gets user information from request.
    Original_url is original link. Not object of the original link.
    """
    ip_address = request.META.get("REMOTE_ADDR")
    user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
    referrer = request.META.get("HTTP_REFERER", "Direct")

    add_url_information.delay(
        original_url=original_url,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
    )
