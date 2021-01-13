# Dictionary
# create a dictionary with the same keys as another, but with the values set to something else
first_dict = {0: False, 1: False}
second_dict = dict.fromkeys(first_dict, True)

print()