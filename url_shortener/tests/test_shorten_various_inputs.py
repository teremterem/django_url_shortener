from unittest.mock import patch

from django.db import DatabaseError, IntegrityError
from django.test import TestCase

from ..models import ShortenedUrl
from ..shortener import shortener_storage
from ..shortener.shortener_core import convert_url_handle_to_number


class TestShortenVariousInputs(TestCase):
    """
    Test shortener_storage.py::shorten_url function against different inputs.
    """

    def test_shorten_url_with_http(self):
        """
        """
        # TODO
        pass
