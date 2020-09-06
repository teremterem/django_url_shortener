"""
Highest URL HANDLE value of length 5:                                 64 ** 5 - 1  ==              1 073 741 823
Highest URL HANDLE value of length 6:                                 64 ** 6 - 1  ==             68 719 476 735
Highest URL HANDLE value of length 7:                                 64 ** 7 - 1  ==          4 398 046 511 103

Biggest positive value of 4-byte signed int:                    256 ** 4 // 2 - 1  ==              2 147 483 647
Biggest positive value of 8-byte signed int (aka signed long):  256 ** 8 // 2 - 1  ==  9 223 372 036 854 775 807

CONCLUSION: numeric representation of URL HANDLE of length 7 can be stored in Postgres as int8 (but not as int4)
"""
import secrets
import string
from urllib.parse import urlparse, urlunparse

URL_ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + '-_'  # 64 distinct characters
URL_HANDLE_LEN = 7


def generate_url_handle():
    """
    https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    secrets library ensures cryptographic random
    """
    return ''.join([secrets.choice(URL_ALPHABET) for _ in range(URL_HANDLE_LEN)])


def convert_url_handle_to_number(url_handle):
    """
    This method expects URL_ALPHABET to be exactly 64 characters big. It is designed to convert string handles to
    numbers as quickly as possible and thus relies on the existence of URL_ALPHABET_TRANSLATIONS table (tuple) as well
    as on the fact that 64 == 2**6 which allows us to leverage from bitwise shift to the left.
    """
    number = 0
    for symbol in url_handle:
        number <<= 6
        number ^= URL_ALPHABET_TRANSLATIONS[ord(symbol)]
    return number


def normalize_long_url(long_url):
    """
    https://stackoverflow.com/a/21659195/2040370
    """
    long_url = long_url.strip()

    parse_result = urlparse(long_url, 'http')

    netloc = parse_result.netloc or parse_result.path
    path = parse_result.path if parse_result.netloc else ''

    return urlunparse((parse_result.scheme, netloc, path, *parse_result[3:]))


def _generate_url_alphabet_translations_tuple():
    trans_list = [None] * (max(ord(c) for c in URL_ALPHABET) + 1)

    for number, symbol in enumerate(URL_ALPHABET):
        trans_list[ord(symbol)] = number

    return tuple(trans_list)  # indexing is faster in a tuple rather than in a list


# This tuple exists to speed up conversion from string handle to number. It is expected to be somewhat bigger than the
# alphabet (64 symbols) because ASCII symbols of the alphabet aren't all adjacent in ASCII table (they are close enough
# to each other and to the beginning of the table, however; plus the whole ASCII table is not too big even if they
# weren't).
URL_ALPHABET_TRANSLATIONS = _generate_url_alphabet_translations_tuple()
