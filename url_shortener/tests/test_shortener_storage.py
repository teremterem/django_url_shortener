from unittest.mock import patch

from django.test import TestCase

from url_shortener.models import ShortenedUrl
from url_shortener.shortener import shortener_storage


class TestShortenerStorage(TestCase):
    """
    Test shortener_storage.py module.
    """

    @patch.object(shortener_storage, 'generate_url_handle', return_value='ba')
    def test_only_one_table_row_1(self, mock_generate_url_handle):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        shortener_storage.shorten_url('someurl1')

        rows = ShortenedUrl.objects.all()
        id_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(id_list, [(64, 'someurl1')])

    @patch.object(shortener_storage, 'generate_url_handle', return_value='ca')
    def test_only_one_table_row_2(self, mock_generate_url_handle):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        shortener_storage.shorten_url('someurl2')

        rows = ShortenedUrl.objects.all()
        id_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(id_list, [(128, 'someurl2')])
