#  Take an address or location and return the closest airport

import sqlite3
from collections import namedtuple

import geopy
import geopy.distance
from geopy.exc import GeocoderTimedOut

import kdtree


def closestAirport(query):
    """

    :param query:
    :return:
    """

    search_coord = None
    searching_nominatim = True

    while searching_nominatim:
        try:
            search_coord = geopy.Nominatim().geocode(query)
            print('Search Coordinate Found:', search_coord)
            if search_coord:
                # searching_nominatim = False
                break
        except GeocoderTimedOut:
            print('Search timed out while waiting for Nominatim.')
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

    tree = kdtree.build_kdtree(airport_list)

    # print(tree)

    closest_node = kdtree.find_nearest_neighbor((search_coord.latitude, search_coord.longitude), tree)

    print('Search Coord:', search_coord, search_coord.latitude, search_coord.longitude)
    print('Closest Coord:', closest_node.location)
    print('Distance:', geopy.distance.vincenty((search_coord.latitude, search_coord.longitude), closest_node.location))
    print('Airport ID:', closest_node.key)
    print('Airport Name:',
          cursor.execute('SELECT DISTINCT name FROM airports WHERE airport_id=?', (closest_node.key,)).fetchone()[
              0])

    return closest_node


if __name__ == '__main__':
    closestAirport('new york, new york')
