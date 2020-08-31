from unittest.mock import patch

from django.test import TestCase

from ..models import ShortenedUrl
from ..shortener import shortener_storage


class TestTestCase(TestCase):
    """
    Test the tests (make sure test interactions with the database are isolated).
    """

    def test_two_table_rows(self):
        ShortenedUrl.objects.create(id=444)
        ShortenedUrl.objects.create(id=333)

        rows = ShortenedUrl.objects.all()
        id_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(id_list, [(333, ''), (444, '')])
