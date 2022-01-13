def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    kw = []  # type: str
    a = 0
    ciphertext = ""
    for i in keyword:
        if 65 <= ord(i) <= 90:
            kw.insert(a, ord(i) - 65)
        else:
            kw.insert(a, ord(i) - 97)
        a += 1
    kwlen = a
    a = 0
    for j in plaintext:
        if a >= kwlen:
            a = 0
        if 65 <= ord(j) <= 90:
            ciphertext += chr((ord(j) - 65 + kw[a]) % 26 + 65)
        else:
            ciphertext += chr((ord(j) - 97 + kw[a]) % 26 + 97)
        a += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    kw = []  # type: str
    a = 0
    plaintext = ""
    for i in keyword:
        if 65 <= ord(i) <= 90:
            kw.insert(a, ord(i) - 65)
        else:
            kw.insert(a, ord(i) - 97)
        a += 1
    kwlen = a
    a = 0
    for j in ciphertext:
        if a >= kwlen:
            a = 0
        if 65 <= ord(j) <= 90:
            if ord(j) - 65 - kw[a] < 0:
                plaintext += chr((ord(j) - 65 - kw[a]) + 91)
            else:
                plaintext += chr(ord(j) - kw[a])
        else:
            if ord(j) - 97 - kw[a] < 0:
                plaintext += chr((ord(j) - 97 - kw[a]) + 123)
            else:
                plaintext += chr(ord(j) - kw[a])
        a += 1
    return plaintext
