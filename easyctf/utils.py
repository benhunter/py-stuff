import hashlib
import string


def ceaser(plaintext, shift):
    '''

    :param plaintext: bytes
    :param shift: int, Number of characters to shift by.
    :return: bytes
    '''
    if type(plaintext) is not bytes:
        raise TypeError('plaintext must be bytes.')
    alphabet = string.ascii_lowercase.encode()
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


def solve_TheOldestTrickintheBook():
    for x in range(26):
        shift = ceaser('tphnriu{l3ar0b3_70_345nr7u_69r67r}'.encode(), x)
        if shift[0] == ord('e'):
            print('Shift', x, 'Result:', shift)


def solve_SoupremeEncoder():
    s = b'68657869745f6d6174655f3164353564653365353435396338613463346138'
    print(hexbytes_to_bytestr(s))


def solve_IntroHashing():
    # file = input('File path and name: ')
    file = 'C:\\Users\\ben\\Downloads\\easyctf-sha512.png'
    with open(file, mode='rb') as f:
        h = hashlib.sha512()
        h.update(f.read())
        print(h.hexdigest())


# Intro: Reverse Engineering
import binascii

key = "qokaQXNN"


def mystery(s):
    r = ""
    for i, c in enumerate(s):
        i_mod_len_of_key = i % len(key)
        select_key = key[i_mod_len_of_key]
        ord_key = ord(select_key)

        i_times_ord_key = i * ord_key
        i_times_ord_key_mod_256 = i_times_ord_key % 256
        ord_c_xor_i_times_ord_key_mod_256 = ord(c) ^ i_times_ord_key_mod_256

        r += chr(ord_c_xor_i_times_ord_key_mod_256)

    b = bytes(r, "utf-8")
    return binascii.hexlify(b)


def reverse_mystery(ciphertext):
    print(ciphertext)
    print(ciphertext.decode())
    hexbytes = binascii.unhexlify(ciphertext)
    print(hexbytes)
    plaintext = hexbytes.decode()

    # plaintext = hexbytes
    return plaintext


# solve_TheOldestTrickintheBook()
# solve_SoupremeEncoder()
# solve_IntroHashing()
print(reverse_mystery(b'650ec2a55a27c38cc2b259c3abc28f4f59c2931a3dc38d7337c3a7410b7ac39135c39cc3a2c29846'))
