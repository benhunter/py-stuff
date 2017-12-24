#  Take an address or location and return the closest airport

import geopy
import geopy.distance
from geopy.exc import GeocoderTimedOut
import sqlite3
import pprint
from collections import namedtuple


class KDNode(namedtuple('KDNode', 'location left_child right_child key')):
    def __repr__(self):
        return pprint.pformat(tuple(self))


def build_kdtree(list, depth=0):
    """
    Credit to implementation at https://en.wikipedia.org/wiki/K-d_tree
    :param list: Must be a list of lists: (((latitude1, longitude1), id1), ((latitude2, longitude2), id2), ...).
    :param depth: The current depth in the K-D Tree.
    :return: KDNode object including its left and right children.
    """
    try:
        k = len(list[0][0])  # assumes all points have the same dimension
    except IndexError as e:
        return None

    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list and choose median as pivot element
    list.sort(key=lambda point: point[0][axis])
    median = len(list) // 2  # choose median

    # Create node and construct subtrees
    return KDNode(
        location=list[median][0],
        left_child=build_kdtree(list[:median], depth + 1),
        right_child=build_kdtree(list[median + 1:], depth + 1),
        key=list[median][1]
    )


def find_nearest_neighbor(coord, kdnode, depth=0):
    """
    Find the nearest neighboor to coord in the K-Depth Tree kdnode
    :param coord: (latitude, longitude)
    :param kdnode: KDNode. kdnode.location = (latitude, longitude)
    :param depth: The current depth in the tree. Determines which axis is used to organize and split the child nodes.
    :return: KDNode
    """

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

    # What is center coord of axis? Difference with search coord determines direction
    # Tree is sorted low left to high right on axis?
    # 10 - 12 = -2, means go right
    # 14 - 8 = 6, means go left
    if kdnode.location[axis] - coord[axis] > 0:
        nearest = find_nearest_neighbor(coord, kdnode.left_child, depth + 1)
        searched_left = True
    else:
        nearest = find_nearest_neighbor(coord, kdnode.right_child, depth + 1)
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
            possible_nearest = find_nearest_neighbor(coord, kdnode.left_child, depth + 1)
        else:
            possible_nearest = find_nearest_neighbor(coord, kdnode.right_child, depth + 1)

    if possible_nearest is None:
        return nearest

    if geopy.distance.vincenty(coord, possible_nearest.location).miles < nearest_miles:
        return possible_nearest

    return nearest


def closestAirport(query):
    """

    :param query:
    :return:
    """
    searching_nominatim = True
    while (searching_nominatim):
        try:
            searchCoord = geopy.Nominatim().geocode(query)
            print(searchCoord)
            if searchCoord:
                searching_nominatim = False
        except GeocoderTimedOut:
            pass

    Point = namedtuple('Point', 'latitude longitude')
    # searchCoord = Point(latitude=39.9, longitude=-104.7) # 39.902534, -104.714531

    conn = sqlite3.connect('openflight.db')
    cursor = conn.cursor()
    cursor.execute('SELECT latitude, longitude, airport_id FROM airports')  # LIMIT 1000')
    airport_db = cursor.fetchall()

    # find column names in a database table
    # names = list(map(lambda x: x[0], cursor.description))
    # names = [description[0] for description in cursor.description]

    airport_list = list(map(lambda airport: ((float(airport[0]), float(airport[1])), airport[2]), airport_db))

    # print(airport_list)
    # airport_list.sort(key=operator.itemgetter(1))
    airport_list.sort(key=lambda airport: airport[0][0])
    # print(airport_list)

    tree = build_kdtree(airport_list)

    # print(tree)

    closestNode = find_nearest_neighbor((searchCoord.latitude, searchCoord.longitude), tree)

    print('Search Coord:', searchCoord, searchCoord.latitude, searchCoord.longitude)
    print('Closest Coord:', closestNode.location)
    print('Distance:', geopy.distance.vincenty((searchCoord.latitude, searchCoord.longitude), closestNode.location))
    print('Airport ID:', closestNode.key)
    print('Airport Name:',
          cursor.execute('SELECT DISTINCT name FROM airports WHERE airport_id=?', (closestNode.key,)).fetchone()[
              0])

    return closestNode


if __name__ == '__main__':
    closestAirport('new york, new york')
