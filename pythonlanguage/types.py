# Dictionary
# create a dictionary with the same keys as another, but with the values set to something else
first_dict = {0: False, 1: False}
second_dict = dict.fromkeys(first_dict, True)

# max of dict gets the max key not max value
third_dict = {1:34, 3:8}
md = max(third_dict)
print(md)  # prints 3 - the max key

# search for the key of a specific value
next((key for key, value in third_dict.items() if value == 8), None)  # fails gracefully
list(third_dict.keys())[list(third_dict.values()).index(8)]  # fast for very large dicts
 

# Slicing
string = "abcdefghijklmnopqrstuvwxyz"

# for index in range(len(string)):
    # print(string[:index], string[index:])

for index in range(len(string) - 1):
    print(string[:index + 1], string[index + 1:])

    

# Insert a list into another list - efficiently?
inner = list(range(3))
outer = list(range(10))
destination_index = 2
# place inner into outer after destination_index
# option 1 fastest?
outer[destination_index + 1 : destination_index + 1] = inner
# option 2
outer = outer[:destination_index + 1] + inner + outer[destination_index + 1:]
# option 3
outer = [*outer[:destination_index + 1], *inner, *outer[destination_index + 1:]]
# option 4
new_outer = outer[:destination_index + 1]
new_outer += inner
new_outer += outer[destination_index + 1:]
outer = new_outer
# fails
outer.insert(destination_index + 1, inner)  # does not unpack inner
outer.insert(destination_index + 1, *inner)  # TODO test unpacking