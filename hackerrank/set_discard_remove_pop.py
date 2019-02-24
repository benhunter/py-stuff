# len_data = 9
len_data = int(input())
# data = set([int(x) for x in "1 2 3 4 5 6 7 8 9".split()])
# data = set([int(x) for x in input().split()])
data = set(map(int, input().split()))
# len_ops = 10
len_ops = int(input())
# ops = """pop
# remove 9
# discard 9
# discard 8
# remove 7
# pop
# discard 6
# remove 5
# pop
# discard 5""".splitlines()

for i in range(len_ops):
    x = input()
    if x == "pop":
        data.pop()
    elif x.split()[0] == "discard":
        data.discard(int(x.split()[1]))
    elif x.split()[0] == "remove":
        data.remove(int(x.split()[1]))

print(sum(data))
