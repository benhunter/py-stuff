file_name = "text.txt"

with open(file_name, 'w') as f:
    for i in range(10):
        f.write(str(i) + '\n')

with open(file_name) as f:
    # text = f.readlines().rstrip()
    # text = f.readlines()
    # print(type(text))
    # print()
    # print(text)
    # print()
    print([line.rstrip() for line in f])
