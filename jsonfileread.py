import json

path = 'jsontest.txt'
dictionary = None

file = open(path, 'r')

dictionary = json.load(file)

print(dictionary)
print(dictionary['key2'])
print(type(dictionary['key2']))