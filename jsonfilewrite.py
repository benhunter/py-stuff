import json

path = 'jsontest.txt'
dictionary = {'key1':'val1', 'key2':'val2', 'list1':('a', 'b', 'c')}

file = open(path, 'w+')

json.dump(dictionary, file)
