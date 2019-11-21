'''
16
1 2 3 4 5 6 7 8 9 10 11 12 13 14 24 52
4
intersection_update 10
2 3 5 6 8 9 1 4 7 11
update 2
55 66
symmetric_difference_update 5
22 7 35 62 58
difference_update 7
11 22 35 55 58 62 66
'''

# Set mutations
input()  # len(set_a)
set_a = set(input().split())
# print("set_a", set_a)
mutation_count = int(input())
# print(mutation_count)

for i in range(mutation_count):
    operation, op_len = input().split()
    set_b = set(input().split())

    if operation == 'update':
        set_a.update(set_b)
    elif operation == 'intersection_update':
        set_a.intersection_update(set_b)
    elif operation == 'symmetric_difference_update':
        set_a.symmetric_difference_update(set_b)
    elif operation == 'difference_update':
        set_a.difference_update(set_b)
    else:
        raise Exception()

    # print(i, set_a, set_b)

# print(set_a)

count = sum(list(map(int, set_a)))
print(count)
