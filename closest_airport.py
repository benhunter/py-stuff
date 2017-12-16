#  Take an address or location and return the closest airport

import geopy
import geopy.distance
import sqlite3
import pprint
import operator
from collections import namedtuple


class AirportKDNode(namedtuple('AirportKDNode', 'location left_child right_child airport_id')):
    def __repr__(self):
        return pprint.pformat(tuple(self))

# airport_list must be a list of lists: (((latitude, longitude), airport_id), ...)
# credit to implementation at https://en.wikipedia.org/wiki/K-d_tree
def kdtree(airport_list, depth=0):
    try:
        k = len(airport_list[0][0])  # assumes all points have the same dimension
    except IndexError as e:
        return None
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list and choose median as pivot element
    airport_list.sort(key=lambda airport: airport[0][axis])
    # airport_list.sort(key=operator.itemgetter([0][axis])) # TODO test itemgetter on sublist

    median = len(airport_list) // 2  # choose median

    # Create node and construct subtrees
    return AirportKDNode(
        location=airport_list[median][0],
        left_child=kdtree(airport_list[:median], depth + 1),
        right_child=kdtree(airport_list[median + 1:], depth + 1),
        airport_id = airport_list[median][1]
    )

def closestAirport(query):
    # searchCoord = geopy.Nominatim().geocode(query)
    Point = namedtuple('Point', 'latitude longitude')
    searchCoord = Point(latitude=63.160499572, longitude=-41.4259986877)

    conn = sqlite3.connect('openflight.db')
    cursor = conn.cursor()
    cursor.execute('SELECT latitude, longitude, airport_id FROM airports') # LIMIT 100000')
    airport_db = cursor.fetchall()

    # find column names in a database table
    # names = list(map(lambda x: x[0], cursor.description))
    # names = [description[0] for description in cursor.description]

    airport_list = list(map(lambda airport: ((float(airport[0]), float(airport[1])), airport[2]), airport_db))

    # print(airport_list)
    # airport_list.sort(key=operator.itemgetter(1))
    airport_list.sort(key=lambda airport: airport[0][0])
    # print(airport_list)

    tree = kdtree(airport_list)

    # print(tree)

    closestNode = find_nearest_neighbor((searchCoord.latitude, searchCoord.longitude), tree)

    print('Search Coord:', searchCoord)
    print('Closest Coord:', closestNode.location)
    print('Distance:', geopy.distance.vincenty((searchCoord.latitude, searchCoord.longitude), closestNode.location))
    print('Airport ID:', closestNode.airport_id)
    print('Airport Name:', cursor.execute('SELECT DISTINCT name FROM airports WHERE airport_id=?', (closestNode.airport_id,)).fetchall())

    return closestNode

# coord = (latitude, longitude)
# kdnode.location = (latitude, longitude)
def find_nearest_neighbor(coord, kdnode, depth=0):

    # 1. Find best leaf node. Save as current best.
    # 2. Unwind recursion up the tree:
    # 2.a. If current node is better, it becomes current best.
    # 2.b. Check the splitting plane for possibility of better node.
    # 2.b.i. If better node is possible, do the entire search on the subtree from current node.
    # 2.b.ii. Continue up the tree.

    if kdnode is None:
        return None

    k = len(kdnode.location)  # assumes all points have the same dimension
    axis = depth % k
    nearest = None
    searched_left = None
    possible_nearest = None

    # what is center coord of axis? Difference with search coord determines direction
    # is tree sorted low left to high right on axis?
    # 10 - 12 = -2, means go right
    # 14 - 8 = 6, means go left
    if kdnode.location[axis] - coord[axis] > 0:
        nearest = find_nearest_neighbor(coord, kdnode.left_child, depth+1)
        searched_left = True
    else:
        nearest = find_nearest_neighbor(coord, kdnode.right_child, depth+1)
        searched_left = False

    if nearest is None:
        return kdnode

    nearest_miles = geopy.distance.vincenty(coord, nearest.location).miles
    current_miles = geopy.distance.vincenty(coord, kdnode.location).miles

    if current_miles < nearest_miles:
        nearest = kdnode
        nearest_miles = current_miles

    # 2.b. Check the splitting plane for possibility of better node.
    # 2.b.i. If better node is possible, do the entire search on the subtree from current node.
    if abs(kdnode.location[axis] - coord[axis]) < abs(nearest.location[axis] - coord[axis]):
        if searched_left:
            possible_nearest = find_nearest_neighbor(coord, kdnode.left_child, depth+1)
        else:
            possible_nearest = find_nearest_neighbor(coord, kdnode.right_child, depth+1)

    if possible_nearest is None:
        return nearest

    if geopy.distance.vincenty(coord, possible_nearest.location).miles < nearest_miles:
        return possible_nearest

    return nearest

    #######
    # if kdnode is None:
    #     return None
    #
    # curr_dist = geopy.distance.vincenty(coord, kdnode.location).miles
    #
    # left_closer = False
    # right_closer = False
    #
    # # Go left or right?
    # if kdnode.left_child is not None:
    #     nearest_left = find_nearest_neighbor(coord, kdnode.left_child)
    #     if geopy.distance.vincenty(coord, nearest_left.location).miles < curr_dist:
    #         left_closer = True # return nearest_left
    #
    # if kdnode.right_child is not None:
    #     nearest_right = find_nearest_neighbor(coord, kdnode.right_child)
    #     if geopy.distance.vincenty(coord, nearest_right.location).miles < curr_dist:
    #         right_closer = True # return nearest_right
    #
    # return kdnode

if __name__ == '__main__':
    closestAirport('1400 Welton St, Denver, CO')
