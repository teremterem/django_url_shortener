URL_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'  # 64 distinct characters

URL_HANDLE_LEN = 10
# number of distinct url handle values:                                64 ** 10 - 1  ==  1152921504606846975
# biggest positive value of 8-byte signed int (aka signed long):  256 ** 8 // 2 - 1  ==  9223372036854775807
#
# (64 ** 10 - 1  <=  256 ** 8 // 2 - 1)  is  True
#
# CONCLUSION: long int representation of URL HANDLE can be stored in postgres as int8
