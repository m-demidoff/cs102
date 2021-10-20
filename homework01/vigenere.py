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
    ciphertext = ""
    k = 0
    while len(keyword) < len(plaintext):
        keyword += keyword[k % len(keyword)]
        k += 1
    alpha_s = [chr(x) for x in range(ord("a"), ord("z") + 1)]
    alpha_c = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
    for i in range(len(plaintext)):
        key = keyword[i]
        shift = 0
        if key in alpha_c:
            shift = alpha_c.index(key)
        elif key in alpha_s:
            shift = alpha_s.index(key)
        symb = plaintext[i]
        if symb in alpha_s:
            ciphertext += alpha_s[(alpha_s.index(symb) + shift) % len(alpha_s)]
        elif symb in alpha_c:
            ciphertext += alpha_c[(alpha_c.index(symb) + shift) % len(alpha_c)]
        else:
            ciphertext += symb
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
    plaintext = ""
    k = 0
    while len(keyword) < len(ciphertext):
        keyword += keyword[k % len(keyword)]
        k += 1
    alpha_s = [chr(x) for x in range(ord("a"), ord("z") + 1)]
    alpha_c = [chr(x) for x in range(ord("A"), ord("Z") + 1)]
    for i in range(len(ciphertext)):
        key = keyword[i]
        shift = 0
        if key in alpha_c:
            shift = alpha_c.index(key)
        elif key in alpha_s:
            shift = alpha_s.index(key)
        symb = ciphertext[i]
        if symb in alpha_s:
            plaintext += alpha_s[(alpha_s.index(symb) - shift) % len(alpha_s)]
        elif symb in alpha_c:
            plaintext += alpha_c[(alpha_c.index(symb) - shift) % len(alpha_c)]
        else:
            plaintext += symb
    return plaintext
