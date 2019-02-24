def test(arg):
    print(str(arg), bool(arg))


if True:
    print("Always True")

if 1:
    print("1 is True")

print(test(1))
print(test(""))
print(test("True"))
print(test("0"))
print(test())
print(test(None))
