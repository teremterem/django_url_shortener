from unittest.mock import patch

from django.test import TestCase

from ..shortener.shortener_utils import generate_url_handle, convert_url_handle_to_number, URL_ALPHABET, \
    URL_HANDLE_LEN, URL_ALPHABET_TRANSLATIONS


class TestShortenerUtils(TestCase):
    """
    Test shortener_utils.py module.
    """

    def test_url_alphabet_size(self):
        """
        Make sure alphabet contains exactly 64 distinct characters.
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

        handles = [generate_url_handle() for _ in range(10)]
        # print(handles)

        self.assertEqual(
            handles,
            ['abcdefg', 'hijklmn', 'opqrstu', 'vwxyzAB', 'CDEFGHI', 'JKLMNOP', 'QRSTUVW', 'XYZ0123', '456789-',
             '_abcdef'],
        )

    def test_generate_url_handle(self):
        """
        Verify that unmocked version of generate_url_handle function works (generates string handles of length 7).
        """
        handle = generate_url_handle()

        self.assertEqual(type(handle), str)
        self.assertEqual(len(handle), 7)

    def test_url_alphabet_translations(self):
        """
        Make sure character to number translations in URL_ALPHABET_TRANSLATIONS tuple roughly make sense.
        """
        self.assertGreaterEqual(len(URL_ALPHABET_TRANSLATIONS), len(URL_ALPHABET))
        self.assertCountEqual(
            [number for number in URL_ALPHABET_TRANSLATIONS if number is not None],
            list(range(len(URL_ALPHABET))),
        )

    def test_convert_url_handle_to_number(self):
        """
        Verify that convert_url_handle_to_number('Hello') returns
        33*64**4 + 4*64**3 + 11*64**2 + 11*64 + 14 == 554742478
        """
        number = convert_url_handle_to_number('Hello')
        self.assertEqual(number, 554742478)
