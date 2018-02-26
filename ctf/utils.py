import itertools
import json
import string
from collections import OrderedDict


def loadjson(file):
    '''
    Loads a JSON formatted file into a dictionary.
    :param file: file name/path. Example 'file.json' or 'c:\data\file.json'
    :return: dict
    '''
    with open(file) as f:
        return json.load(f)


def solve_frequency(inbytes):
    cipher = inbytes.upper()

    # analyze frequncy and build substitution table
    # English letter frequency:
    common_freq = b'etaoinshrdlcumwfgypbvkjxqz'.upper()  # standard

    # count occurrences in cipher
    freq_table = {}
    for char in string.ascii_uppercase.encode():
        n = cipher.count(char)
        if n > 0:
            freq_table[char] = n
        print(char, n)
    print('freq_table', freq_table)

    freq_table = OrderedDict(sorted(freq_table.items(), key=lambda t: t[1], reverse=True))
    print('ordered freq_table', freq_table)

    for i in freq_table:
        print(chr(i), ':', freq_table[i])

    # build substitution table
    substitution_table = OrderedDict()

    for index, char in enumerate(freq_table):
        substitution_table[char] = common_freq[index]

    print('substitution_table', substitution_table)
    print('cipher : plain')
    for i in substitution_table:
        print(chr(i), ':', chr(substitution_table[i]))

    # apply substitution table
    for i in range(len(cipher)):
        substitution_table.setdefault(cipher[i], cipher[i])
        print(chr(substitution_table[cipher[i]]), end='')


def stringwithspacescommastolist(the_string):
    return list(itertools.chain.from_iterable(map(lambda x: x.strip().split(), the_string.split(','))))


def int_ignore_crap(list_of_string):
    # print(list_of_string)
    int_list = []
    for the_string in list_of_string:
        try:
            # print(the_string)
            # print(int(the_string))
            int_list.append(int(the_string))
        except ValueError:
            pass
    return int_list


if __name__ == '__main__':
    solve_frequency(
        b'Nhyob vfs a ccy dv vjhezmv bymw decr xfgv h dfhprgc voeqtj domm gc hkrsddw rr zbu ghkqb pz nclxqdwtpuqr')
