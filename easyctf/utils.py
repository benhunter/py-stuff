import string


def ceaser(plaintext, shift, mode='encode'):
    '''
    Ceaser cipher encoder and decoder.
    :param plaintext: bytes
    :param shift: int, Number of characters to shift by.
    :param mode: 'encode' from plain to cipher, 'decode' from cipher to plain.
    :return: bytes
    '''
    if type(plaintext) is not bytes:
        raise TypeError('plaintext must be bytes.')
    alphabet = string.ascii_lowercase.encode()
    if mode == 'encode':
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    elif mode == 'decode':
        shift *= -1
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = bytes.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)


def groups(seq, length):
    '''
    :param seq: A slicable object like string or list.
    :param length: The length of the groups
    :return:
    '''
    for i in range(0, len(seq), length):
        # print(i)
        yield seq[i:i + length]


def hexbytes_to_bytestr(bytes_data):
    l = list(map(lambda x: chr(int(x, 16)).encode(), groups(bytes_data, 2)))
    s = b''.join(l)
    return s

