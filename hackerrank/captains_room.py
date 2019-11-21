# https://www.hackerrank.com/challenges/py-the-captains-room/problem

'''
5
1 2 3 6 5 4 4 2 5 3 6 1 6 5 3 2 4 1 2 5 1 4 3 6 8 4 3 1 5 6 2
'''
k = int(input())
guests = list(map(int, input().split()))
possible_captains = set(guests)
unique_guests = set()

while len(guests) > 0:
    next_guest = guests.pop()
    # print("next_guest", next_guest)
    # if len(possible_captains) < 100: print("possible_captains", possible_captains)
    # print("unique_guests", unique_guests)
    guest_set = set()
    guest_set.add(next_guest)


    guest_intersection = unique_guests.intersection(guest_set)
    # print(guest_intersection)
    len_intersection = len(guest_intersection)

    if len_intersection == 1:
        # print('removing from possible_captains:', next_guest)
        possible_captains.discard(next_guest)
    elif len_intersection == 0:
        # print('updating unique_guests:', next_guest)
        unique_guests.update(guest_set)
    # print()

# print(possible_captains)
print(possible_captains.pop())



