from unittest.mock import patch

from django.test import TestCase

from ..models import ShortenedUrl
from ..shortener import shortener_storage
from ..shortener.shortener_core import convert_url_handle_to_number


class TestShortenerStorage(TestCase):
    """
    Test shortener_storage.py module.
    """

    @patch.object(shortener_storage, 'generate_url_handle')
    def test_shorten_url_with_mocked_handle_generator(self, mock_generate_url_handle):
        """
        Make sure shorten_url persists ShortenedUrl objects with proper values (mocked handle generator).
        """
        mock_generate_url_handle.return_value = 'ca'
        shortener_storage.shorten_url('someurl2')

        mock_generate_url_handle.return_value = 'ba'
        shortener_storage.shorten_url('someurl1')

        rows = ShortenedUrl.objects.all()
        id_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(id_list, [(64, 'someurl1'), (128, 'someurl2')])

    def test_shorten_url(self):
        """
        Make sure shorten_url persists ShortenedUrl object with proper values (no mocks).
        """
        url_handle = shortener_storage.shorten_url('https://someurl3.io/index.html')

        rows = ShortenedUrl.objects.all()
        id_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(id_list, [(convert_url_handle_to_number(url_handle), 'https://someurl3.io/index.html')])
