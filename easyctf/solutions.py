import binascii
import hashlib
import itertools
import string
from collections import OrderedDict

import utils


def solve_TheOldestTrickintheBook():
    for x in range(26):
        shift = utils.ceaser('tphnriu{l3ar0b3_70_345nr7u_69r67r}'.encode(), x, mode='encode')
        if shift[0] == ord('e'):
            print('Shift', x, 'Result:', shift)


def solve_SoupremeEncoder():
    s = b'68657869745f6d6174655f3164353564653365353435396338613463346138'
    print(utils.hexbytes_to_bytestr(s))


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


# Intro: Reverse Engineering - solution
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
    print(utils.ceaser(cipher, N, mode='decode').decode())


def solve_Substitute():
    cipher = b'FI! XJWCYIUSINLIGH QGLE TAMC A XCU NSAO NID EPC WEN AXM JL EIEASSF HDIGM IN JEL JXOCXGJEF. EPJL JL ASLI EPC LCWIXM HDIYSCT CZCD TAMC NID CALFWEN. PCDC: CALFWEN{EPJL_JL_AX_CALF_NSAO_EI_OGCLL} GLC WAHJEAS SCEECDL.'

    # frequency analysis
    # English letter frequency:
    common_freq = b'etaoinshrdlcumwfgypbvkjxqz'.upper()  # standard
    common_freq = b'estaoiflrnyucdhpgmwbjv****'.upper()  # modified

    # count occurrences in cipher
    freq_table = {}
    for char in string.ascii_uppercase.encode():
        n = cipher.count(char)
        if n > 0:
            freq_table[char] = n
        # print(char, n)
    # print('freq_table', freq_table)

    freq_table = OrderedDict(sorted(freq_table.items(), key=lambda t: t[1], reverse=True))
    print('ordered freq_table', freq_table)
    for i in freq_table:
        print(chr(i), ':', freq_table[i])

    # build substitution table
    substitution_table = OrderedDict()

    for index, char in enumerate(freq_table):
        substitution_table[char] = common_freq[index]

    print('substitution_table', substitution_table)
    for i in substitution_table:
        print(chr(i), ':', chr(substitution_table[i]))

    # replace cipher with chars from substitution table
    for i in range(len(cipher)):
        substitution_table.setdefault(cipher[i], cipher[i])
        print(chr(substitution_table[cipher[i]]), end='')


def solve_xor():
    cipher = b'Y]OE_HZGWJQD^XTQF[W]IQTMH]EPEPXTWA'
    for n in range(256):
        b = b''
        for i in cipher:
            b += chr(i ^ n).encode()
            # print(chr(i ^ n), end='')
        if chr(b[0]) == 'e':
            print(b.decode())


def solve_ProgrammingSubsetCounting():
    # N, S = [int(i) for i in input().split()]
    # data = [int(i) for i in input().split()]
    N = 6
    S = 5
    data = [2, 4, 1, 1, 1, 2]
    # print(N, S, data)

    # one way to do it
    solutions = 0
    for i in range(1, len(data) + 1):
        for combo in itertools.combinations(data, i):
            if sum(combo) == S:
                # print('Solution:', combo)
                solutions += 1
    print(solutions)

    # TODO one liner with iterators and list comprehensions?
