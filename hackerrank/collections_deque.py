from collections import deque

len_ops = int(input())
data = deque()

for i in range(len_ops):
    command = ""
    item = ""
    line = input()

    if len(line.split()) > 1:
        command, item = line.split()
    else:
        command = line

    if command == "append":
        data.append(item)
    elif command == "appendleft":
        data.appendleft(item)
    elif command == "pop":
        data.pop()
    elif command == "popleft":
        data.popleft()

print(" ".join(data))
