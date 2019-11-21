# https://www.hackerrank.com/domains/python?filters%5Bsubdomains%5D%5B%5D=py-sets

# Set Union
input()
first = set(map(int, input().split()))
input()
second = set(map(int, input().split()))

print(len(first.union(second)))


# Set Intersection
input()
first = set(input().split())
input()
second = set(input().split())

print(len(first.intersection(second)))

# Set Difference
input()
english = set(input().split())
input()
french = set(input().split())

print(len(english.difference(french)))

# Set Symmetric Difference
input()
english = set(input().split())
input()
french = set(input().split())

print(len(english.symmetric_difference(french)))
