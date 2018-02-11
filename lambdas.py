# https://www.youtube.com/watch?v=OLH3L285EiY
# https://gist.github.com/vakila/3d5cebaebf01c4c77b289b9a0388e3c8
# https://ep2017.europython.eu/conference/talks/mary-had-a-little-lambda

# print((lambda x: x+1)(5))

zero = lambda f: lambda x: x
print(zero)
print(zero(0)(0))
one = lambda f: lambda x: f(x)
two = lambda f: lambda x: f(f(x))
three = lambda f: lambda x: f(f(f(x)))

to_int = lambda n: n(lambda i: i + 1)(0)

print(to_int(zero))
print(to_int(one))
print(to_int(two))

succ = lambda n: lambda f: lambda x: f(n(f)(x))
four = succ(three)
five = succ(four)
print(to_int(four))

eight = succ(succ(succ(succ(four))))

add = lambda n: lambda m: lambda f: lambda x: m(f)(n(f)(x))

ten = add(eight)(two)
print(to_int(ten))

mult = lambda n: lambda m: lambda f: lambda x: m(n(f))(x)

twelve = mult(three)(four)

print(to_int(twelve))

power = lambda n: lambda m: lambda f: lambda x: m(n)(f)(x)
power = lambda n: lambda m: m(n)

print(to_int(power(two)(three)))

answer = add(ten)(power(two)(five))
print(to_int(answer))

ifthenelse = lambda cond: lambda then_do: lambda else_do: cond(then_do)(else_do)

troo = lambda then_do: lambda else_do: then_do
falz = lambda then_do: lambda else_do: else_do

tired = troo
coffees_today = ifthenelse(tired)(three)(one)
print(to_int(coffees_today))

opposite = lambda boolean: lambda thn: lambda els: boolean(els)(thn)
to_bool = lambda boolean: boolean(True)(False)

print(to_bool(troo))

is_zero = lambda n: n(lambda _: falz)(troo)
print(to_bool(is_zero(one)))

is_even = lambda n: n(opposite)(troo)
print(to_bool(is_even(three)))

both = lambda boola: lambda boolb: boola(boolb)(boola)
print(to_bool(both(troo)(troo)))
print(to_bool(both(troo)(falz)))

both = lambda boola: lambda boolb: boola(boola)(boolb)
print(to_bool(both(troo)(troo)))
print(to_bool(both(troo)(falz)))
print(to_bool(both(falz)(falz)))

make_pair = lambda left: lambda right: lambda f: f(left)(right)

left = lambda pair: pair(troo)
right = lambda pair: pair(falz)
print(to_int(right(make_pair(three)(two))))

nil = make_pair(troo)(troo)

# a list will have the form
# (is_empty, (head, tail))

# only nil will have troo as left element
is_empty = left

print(to_bool(is_empty(nil)))

prepend = lambda item: lambda l: make_pair(falz)(make_pair(item)(l))

head = lambda l: left(right(l))
tail = lambda l: right(right(l))

coffees_day_1 = prepend(two)(nil)
coffees_per_day = prepend(three)(prepend(one)(coffees_day_1))
print(to_int(head(tail(coffees_per_day))))
