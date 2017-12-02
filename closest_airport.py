#  Take an address or location and return the closest airport

import geopy, sqlite3

def closestAirport(query):
    # searchCoord = geopy.Nominatim().geocode(query)
    searchCoord = geopy.Nominatim().geocode(query)

    conn = sqlite3.connect('openflight.db')
    cursor = conn.cursor()
    # cursor.execute('')

    return searchCoord

if __name__ == '__main__':
    print(closestAirport('1400 Welton St, Denver, CO'))


