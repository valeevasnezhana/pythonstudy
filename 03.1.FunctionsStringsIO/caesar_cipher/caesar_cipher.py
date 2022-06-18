# def caesar_encrypt(message: str, n: int) -> str:
#     """Encrypt message using caesar cipher
#     :param message: message to encrypt
#     :param n: shift
#     :return: encrypted message
#     """
# result = ''
# low = int(ord("a")) - 1
# up = int(ord("A")) - 1
# alphabet_len = 26
# for symbol in list(message):
#     ord_s = int(ord(symbol))
#     if low < ord_s <= low + alphabet_len:
#         ord_s = (ord_s - low + n) % alphabet_len + low
#         if ord_s == low:
#             ord_s += alphabet_len
#         result = result + chr(ord_s)
#     elif up < ord_s <= up + alphabet_len:
#         ord_s = (ord_s - up + n) % alphabet_len + up
#         if ord_s == up:
#             ord_s += alphabet_len
#         result = result + chr(ord_s)
#     else:
#         result = result + symbol
# return result
from string import ascii_lowercase, ascii_uppercase, ascii_letters


def make_shift(shift: int) -> str:
    return ascii_lowercase[shift:] + ascii_lowercase[:shift] + ascii_uppercase[shift:] + ascii_uppercase[:shift]


def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    table = message.maketrans(ascii_letters, make_shift(n))
    return message.translate(table)
