from django.db import transaction

from .shortener_core import generate_url_handle, convert_url_handle_to_number
from ..models import ShortenedUrl


@transaction.atomic
def shorten_url(long_url):
    url_handle = generate_url_handle()
    ShortenedUrl.objects.create(
        id=convert_url_handle_to_number(url_handle),
        long_url=long_url,
    )
    return url_handle
