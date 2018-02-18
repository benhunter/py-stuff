# string = ''.join(list(map(lambda x: str(x), [0,1,2,3,4,5])))
# string = ''.join(list(map(lambda x: str(x), list(map(lambda x: x, [1])))))
# print(string)


# map(lambda n: (lambda f, *a: f(f, *a))(lambda rec, n: 1 if n == 0 else n*rec(rec, n-1), n), range(10))

# (lambda a:lambda v:a(a,v))(lambda s,x:1 if x==0 else x*s(s,x-1))(10)


