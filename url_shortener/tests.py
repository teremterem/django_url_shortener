from unittest.mock import patch

from django.test import TestCase

from url_shortener.models import ShortenedUrl
from url_shortener.shortener_core import URL_ALPHABET, URL_HANDLE_LEN, generate_url_handle


class TestTestCase(TestCase):
    """
    Test the tests (make sure test interactions with the database are isolated).
    """

    def test_only_one_table_row_1(self):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        ShortenedUrl.objects.create(url_uuid='uuid1')

        rows = ShortenedUrl.objects.all()
        uuid_list = [u.url_uuid for u in rows]
        self.assertCountEqual(uuid_list, ['uuid1'])

    def test_only_one_table_row_2(self):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        ShortenedUrl.objects.create(url_uuid='uuid2')

        rows = ShortenedUrl.objects.all()
        uuid_list = [u.url_uuid for u in rows]
        self.assertCountEqual(uuid_list, ['uuid2'])

    def test_two_table_rows(self):
        ShortenedUrl.objects.create(url_uuid='uuid3')
        ShortenedUrl.objects.create(url_uuid='uuid4')

        rows = ShortenedUrl.objects.all()
        uuid_list = [u.url_uuid for u in rows]
        self.assertCountEqual(uuid_list, ['uuid3', 'uuid4'])


class TestShortenerCore(TestCase):
    """
    Test shortener_core.py module.
    """

    def test_url_alphabet_size(self):
        """
        Make sure alphabet contains 64 distinct characters.
        """
        self.assertEqual(len({c for c in URL_ALPHABET}), 64)
        self.assertEqual(len(URL_ALPHABET), 64, msg='duplicate characters found in URL_ALPHABET')

    def test_url_handle_storable_in_int8(self):
        """
        Make sure URL handle can be stored in Postgres int8.
        """
        self.assertLessEqual(
            len(URL_ALPHABET) ** URL_HANDLE_LEN - 1,
            256 ** 8 // 2 - 1,
            msg='URL handle cannot be stored in Postgres int8',
        )

    @patch('secrets.choice')
    def test_generate_url_handle_mocked_secrets(self, mock_secrets_choice):
        """
        Verify that url handles are predictable when secrets.choice is mocked (this test serves as an "alert" to draw
        developer's attention in case behaviour of generate_url_handle function changes for some reason).
        """
        char_pos = -1

        def _fake_choice(alph):
            nonlocal char_pos
            char_pos += 1
            return alph[char_pos % len(alph)]

        mock_secrets_choice.side_effect = _fake_choice

        handles = [generate_url_handle() for _ in range(7)]
        # print(handles)

        self.assertEqual(
            handles,
            ['abcdefghij', 'klmnopqrst', 'uvwxyzABCD', 'EFGHIJKLMN', 'OPQRSTUVWX', 'YZ01234567', '89-_abcdef'],
        )

    def test_generate_url_handle(self):
        """
        Verify that unmocked version of generate_url_handle function works (generates string handles of length 10).
        """
        handle = generate_url_handle()

        self.assertEqual(type(handle), str)
        self.assertEqual(len(handle), 10)

    def test_url_alphabet_translations(self):
        """
        Make sure character to number translations in URL_ALPHABET_TRANSLATIONS tuple roughly make sense.
        """
        pass
