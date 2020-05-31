# string = ''.join(list(map(lambda x: str(x), [0,1,2,3,4,5])))
# string = ''.join(list(map(lambda x: str(x), list(map(lambda x: x, [1])))))
# print(string)


# map(lambda n: (lambda f, *a: f(f, *a))(lambda rec, n: 1 if n == 0 else n*rec(rec, n-1), n), range(10))

# (lambda a:lambda v:a(a,v))(lambda s,x:1 if x==0 else x*s(s,x-1))(10)

print('etaoinshrdlcumwfgypbvkjxqz'.upper())

string = ''
import itertools

splitstring = list(itertools.chain.from_iterable(map(lambda x: x.strip().split(), string.split(','))))
print(splitstring)


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


# number = list(map(lambda x: int(x), splitstring))
print(sum(int_ignore_crap(splitstring)))
