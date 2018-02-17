import binascii
import hashlib
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
def mystery(s, key="qokaQXNN"):
    print('mystery', s)
    # r = ""
    # for i, c in enumerate(s):
    #     print(c, type(c), ord(c), end=' ')
    #
    #     i_mod_len_of_key = i % len(key)
    #     select_key = key[i_mod_len_of_key]
    #     ord_key = ord(select_key)
    #
    #     i_times_ord_key = i * ord_key
    #     i_times_ord_key_mod_256 = i_times_ord_key % 256
    #     ord_c_xor_i_times_ord_key_mod_256 = ord(c) ^ i_times_ord_key_mod_256
    #
    #     # print('in for loop', i, c, i_times_ord_key_mod_256, ord_c_xor_i_times_ord_key_mod_256, chr(ord_c_xor_i_times_ord_key_mod_256))
    #     print('xor', i_times_ord_key_mod_256, '=', ord_c_xor_i_times_ord_key_mod_256)
    #
    #     next = chr(ord_c_xor_i_times_ord_key_mod_256)
    #     print('next', next)
    #     r += next
    #
    # b = bytes(r, "utf-8")
    # print('mystery', b)
    # print('mystery', type(b))
    # return binascii.hexlify(b)
    r = ""
    for i, c in enumerate(s):
        xor = ord(c) ^ ((i * ord(key[i % len(key)])) % 256)
        next = chr(xor)
        print(next,
              hex(xor),
              xor,
              'xor',
              ((i * ord(key[i % len(key)])) % 256),
              '=',
              xor ^ ((i * ord(key[i % len(key)])) % 256),
              hex(xor ^ ((i * ord(key[i % len(key)])) % 256)),
              chr(xor ^ ((i * ord(key[i % len(key)])) % 256)),
              end=' ')

        r += next
        print(r, bytes(r, "utf-8"))

    b = bytes(r, "utf-8")
    print('mystery', b)
    print('mystery', type(b))
    print('mystery', b.decode())
    h = binascii.hexlify(b)
    print('mystery hex:', h)
    return h


def reverse_mystery(ciphertext, key="qokaQXNN"):
    print('reversing', ciphertext)
    # print(ciphertext)
    # print(ciphertext.decode())
    unhexbytes = binascii.unhexlify(ciphertext).decode('utf-8')

    print('unhex', unhexbytes)
    print('unhex', type(unhexbytes))
    # print('unhex', unhexbytes.decode('utf-8'))

    plaintext = ''
    for i, c in enumerate(unhexbytes):
        print(c, type(c), ord(c), end=' ')

        i_mod_len_of_key = i % len(key)
        select_key = key[i_mod_len_of_key]
        ord_key = ord(select_key)
        i_times_ord_key = i * ord_key
        i_times_ord_key_mod_256 = i_times_ord_key % 256
        # mystery is same to here...
        ord_c_xor_i_times_ord_key_mod_256 = ord(c) ^ i_times_ord_key_mod_256  # original
        # c_xor_i_times_ord_key_mod_256 = c ^ i_times_ord_key_mod_256  # new

        print('xor', i_times_ord_key_mod_256, '=', ord_c_xor_i_times_ord_key_mod_256)

        next = chr(ord_c_xor_i_times_ord_key_mod_256)
        print('next', next)
        plaintext += next
        print('plaintext', plaintext)

    # plaintext = hexbytes
    return plaintext


def solve_IntroReverseEngineering():
    print(reverse_mystery('650ec2a55a27c38cc2b259c3abc28f4f59c2931a3dc38d7337c3a7410b7ac39135c39cc3a2c29846'))
    # print('Reverse:', reverse_mystery('650ec2a5'))
    print()
    print(mystery(
        reverse_mystery('650ec2a55a27c38cc2b259c3abc28f4f59c2931a3dc38d7337c3a7410b7ac39135c39cc3a2c29846')).decode())
    print('650ec2a55a27c38cc2b259c3abc28f4f59c2931a3dc38d7337c3a7410b7ac39135c39cc3a2c29846')
    print()
    # print(mystery('eaea'))
    # print(mystery(reverse_mystery('650ec2a55a27c38cc2b259c3abc28f4f59c2931a3dc38d7337c3a7410b7ac39135c39cc3a2c29846')).decode() == '650ec2a55a27c38cc2b259c3abc28f4f59c2931a3dc38d7337c3a7410b7ac39135c39cc3a2c29846')
    # print(bytes.maketrans(b'', b''))


def solve_ProgrammingOverandOver():
    N = int(input())
    print('over' if N == 1 else ' and '.join(['over' for i in range(N)]), end='')


def solve_ProgrammingTeachingOldTricksNewDogs():
    N = int(input())
    cipher = input().encode()
    # N = 6
    # cipher = 'o rubk kgyeizl'.encode()
    print(ceaser(cipher, N, mode='decode').decode())
