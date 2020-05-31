import geopy


def location_to_latlong(location):
    '''Convert a location to latitude/longitude.

    location: String of location. Ex: zip code "10101", street address, city and state. Or coordinate.

    Returns latitude/longitude as a list of floating points [ xxx.xxx, xxx.xxx ] '''

    result = geopy.geocoders.Nominatim().geocode(location)

    return [result.latitude, result.longitude]

if __name__ == '__main__':
    print(location_to_latlong("1400 Welton St, Denver, CO"))