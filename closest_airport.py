#  Take an address or location and return the closest airport

import geopy, sqlite3

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
