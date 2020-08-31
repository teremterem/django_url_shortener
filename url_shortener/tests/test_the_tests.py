from unittest.mock import patch

from django.test import TestCase

from ..models import ShortenedUrl
from ..shortener import shortener_storage


class TestTestCase(TestCase):
    """
    Test the tests (make sure test interactions with the database are isolated).
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

    def test_two_table_rows(self):
        ShortenedUrl.objects.create(id=444)
        ShortenedUrl.objects.create(id=333)

        rows = ShortenedUrl.objects.all()
        id_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(id_list, [(333, ''), (444, '')])
