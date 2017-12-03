#  Take an address or location and return the closest airport

import geopy
import sqlite3
import pprint
from collections import namedtuple


class AirportKDNode(namedtuple('AirportKDNode', 'location left_child right_child airport_id')):
    def __repr__(self):
        return pprint.pformat(tuple(self))

# airport_list must be a list with the first element containing another list of (latitude, longitude)
def kdtree(airport_list, depth=0):
    try:
        k = len(airport_list[0])  # assumes all points have the same dimension
    except IndexError as e:  # if not point_list:
        return None
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point list and choose median as pivot element
    point_list.sort(key=itemgetter(axis))
    median = len(point_list) // 2  # choose median

    # Create node and construct subtrees
    return Node(
        location=point_list[median],
        left_child=kdtree(point_list[:median], depth + 1),
        right_child=kdtree(point_list[median + 1:], depth + 1)
    )

def closestAirport(query):
    # searchCoord = geopy.Nominatim().geocode(query)
    searchCoord = geopy.Nominatim().geocode(query)

    conn = sqlite3.connect('openflight.db')
    cursor = conn.cursor()
    cursor.execute('SELECT airport_id, latitude, longitude FROM airports')
    airportList = cursor.fetchall()
    print(len(airportList))

    # for row in airportList:
    #     print(row)

    # find column names in a database table
    # names = list(map(lambda x: x[0], cursor.description))
    # names = [description[0] for description in cursor.description]

    return searchCoord

if __name__ == '__main__':
    print(closestAirport('1400 Welton St, Denver, CO'))
