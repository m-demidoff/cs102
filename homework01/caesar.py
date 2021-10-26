import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for c in plaintext:

        # проверить, является ли символ заглавной буквой
        if c.isupper():

            c_index = ord(c) - ord("A")

            # выполнить отрицательный сдвиг
            new_index = (c_index + shift) % 26

            # преобразовать в новый символ
            new_unicode = new_index + ord("A")

            new_character = chr(new_unicode)

            # добавление к простой строке
            ciphertext += new_character

        elif c.islower():
            # найти положение в 0-25
            c_unicode = ord(c)

            c_index = ord(c) - ord("a")

            # выполнить отрицательный сдвиг
            new_index = (c_index + shift) % 26

            # преобразовать в новый символ
            new_unicode = new_index + ord("a")

            new_character = chr(new_unicode)

            # добавление к простой строке
            ciphertext += new_character
        elif c.isdigit():

            # если это число, сдвинуть его фактическое значение
            c_new = int(c)

            ciphertext += str(c_new)

        else:

            # если нет ни алфавита, ни числа, оставьте все как есть
            ciphertext += c
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for c in ciphertext:
        if c.isupper():

            c_index = ord(c) - ord("A")

            new_index = (c_index - shift) % 26

            new_unicode = new_index + ord("A")

            new_character = chr(new_unicode)

            plaintext += new_character

        elif c.islower():

            c_unicode = ord(c)

            c_index = ord(c) - ord("a")

            new_index = (c_index - shift) % 26

            new_unicode = new_index + ord("a")

            new_character = chr(new_unicode)

            plaintext += new_character
        elif c.isdigit():
            c_new = int(c)

            plaintext += str(c_new)
        else:
            plaintext += c
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
