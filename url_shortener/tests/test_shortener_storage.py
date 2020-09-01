from unittest.mock import patch

from django.db import DatabaseError
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
        tuple_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(tuple_list, [(64, 'someurl1'), (128, 'someurl2')])
        self.assertEqual(mock_generate_url_handle.call_count, 2)

    def test_shorten_url(self):
        """
        Make sure shorten_url persists ShortenedUrl object with proper values (no mocks).
        """
        url_handle = shortener_storage.shorten_url('https://someurl3.io/index.html')

        rows = ShortenedUrl.objects.all()
        tuple_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(
            tuple_list, [(convert_url_handle_to_number(url_handle), 'https://someurl3.io/index.html')]
        )

    @patch.object(shortener_storage, 'generate_url_handle')
    def test_shorten_url_collision_of_handle(self, mock_generate_url_handle):
        """
        Make sure shorten_url retries handle generation up to 5 times in case of collision (64**7 distinct values is
        not too many - collisions are possible).
        """

        def _fake_generate():
            nonlocal generate_count
            generate_count += 1
            if generate_count > 2:  # change value issuing two identical url handles
                return 'ea'
            return 'da'

        mock_generate_url_handle.side_effect = _fake_generate

        generate_count = 0
        shortener_storage.shorten_url('http://someurl4/')
        generate_count = 0
        shortener_storage.shorten_url('http://someurl5/')

        rows = ShortenedUrl.objects.all()
        tuple_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(tuple_list, [(192, 'http://someurl4/'), (256, 'http://someurl5/')])
        self.assertEqual(mock_generate_url_handle.call_count, 1 + 3)

    @patch.object(shortener_storage, 'generate_url_handle')
    def test_shorten_url_more_than_5_collisions(self, mock_generate_url_handle):
        """
        Make sure shorten_url does not retry handle generation more than 5 times (protect ourselves from an accidental
        infinite loop, for example).
        """
        mock_generate_url_handle.return_value = 'fa'
        shortener_storage.shorten_url('http://someurl6/')
        shortener_storage.shorten_url('http://someurl7/')

        rows = ShortenedUrl.objects.all()
        tuple_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(tuple_list, [(192, 'http://someurl4/')])

    @patch.object(shortener_storage, 'generate_url_handle')
    def test_shorten_url_some_other_exception(self, mock_generate_url_handle):
        """
        Make sure an arbitrary exception doesn't lead to retries (retries are only for collisions).
        """

        def _raise_error():
            raise DatabaseError()

        mock_generate_url_handle.side_effect = _raise_error
        shortener_storage.shorten_url('http://someurl8/')
        shortener_storage.shorten_url('http://someurl9/')

        rows = ShortenedUrl.objects.all()
        tuple_list = [(row.id, row.long_url) for row in rows]
        self.assertCountEqual(tuple_list, [(192, 'http://someurl4/')])
