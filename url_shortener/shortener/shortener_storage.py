from django.db import transaction, IntegrityError

from .shortener_core import generate_url_handle, convert_url_handle_to_number
from ..models import ShortenedUrl

SHORTEN_ATTEMPT_COUNT = 5


def shorten_url(long_url):
    """
    64**7 distinct values is not too many - collisions are possible. For this reason this function will try to generate
    url handle and attempt to store it up to 5 times (only one time if collision doesn't happen).
    """
    for _ in range(SHORTEN_ATTEMPT_COUNT):
        integrity_error = None
        url_handle = generate_url_handle()
        try:
            with transaction.atomic(savepoint=True):
                ShortenedUrl.objects.create(
                    id=convert_url_handle_to_number(url_handle),
                    long_url=long_url,
                )
        except IntegrityError as e:
            integrity_error = e
            continue  # looks like generated url_handle already exists - retrying...
        break  # no collision - exiting the loop...

    if integrity_error:
        # integrity error persisted even after five attempts - re-raising...
        raise integrity_error

    return url_handle


def expand_url(url_handle):
    try:
        return ShortenedUrl.objects.get(id=convert_url_handle_to_number(url_handle)).long_url
    except ShortenedUrl.DoesNotExist:
        return None
