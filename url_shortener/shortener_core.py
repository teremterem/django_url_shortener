"""
https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
"""
import secrets
import string

# Number of distinct url handle values:                                64 ** 10 - 1  ==  1152921504606846975
# Biggest positive value of 8-byte signed int (aka signed long):  256 ** 8 // 2 - 1  ==  9223372036854775807
#
# (64 ** 10 - 1  <=  256 ** 8 // 2 - 1)  is  True
#
# CONCLUSION: numberic representation of URL HANDLE can be stored in Postgres as int8
URL_ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + '-_'  # 64 distinct characters
URL_HANDLE_LEN = 10

MIN_ORD = min(ord(c) for c in URL_ALPHABET)
MAX_ORD = max(ord(c) for c in URL_ALPHABET)


def _generate_url_alphabet_translations():
    trans_list = [None] * (MAX_ORD - MIN_ORD + 1)

    for digit, chr in enumerate(URL_ALPHABET):
        trans_list[ord(chr) - MIN_ORD] = digit

    return tuple(trans_list)


URL_ALPHABET_TRANSLATIONS = _generate_url_alphabet_translations()


def generate_url_handle():
    return ''.join([secrets.choice(URL_ALPHABET) for _ in range(URL_HANDLE_LEN)])


def convert_url_handle_to_number(url_handle):
    """
    This method expects URL_ALPHABET to be exactly 64 characters big
    """
    # TODO
    pass
