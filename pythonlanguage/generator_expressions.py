# Generator Expressions

s = sum(x*x for x in range(3))
print(s)

xvec = [10, 20, 30]
yvec = [7, 5, 3]
s = sum(x*y for x,y in zip(xvec, yvec))
print(s)