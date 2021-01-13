


def func(test_obj):
    test_obj[0] = "CHANGED"
    # return

a_list = ["one", "two"]
func(a_list)

print(a_list)
