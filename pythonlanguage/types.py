# Dictionary
# create a dictionary with the same keys as another, but with the values set to something else
first_dict = {0: False, 1: False}
second_dict = dict.fromkeys(first_dict, True)


# Slicing
string = "abcdefghijklmnopqrstuvwxyz"

# for index in range(len(string)):
    # print(string[:index], string[index:])

for index in range(len(string) - 1):
    print(string[:index + 1], string[index + 1:])
    