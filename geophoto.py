# https://github.com/collective/collective.geo.exif/blob/master/collective/geo/exif/readexif.py
# KML Docs: https://developers.google.com/kml/documentation/kml_tut
# KML Schema: http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd
# KML Sample: https://developers.google.com/kml/documentation/KML_Samples.kml


from os import walk
from pprint import pprint

import exifgps  # NOT Python 3 ready (uses print statement)
import exifread
from PIL import Image
from PIL.ExifTags import TAGS
from fastkml import kml  # seems more current than pyKML
from shapely.geometry import Point

# target = '~/Drive/Class River/'  # relative paths don't seem to work?
target = '//home/infinite/Drive/Class River/'
# photo_path = 'E:\\google drive\\Photos and Videos\\Class River\\IMG_1406.JPG'
photo_path = '//home/infinite/Drive/Class River/IMG_1468.JPG'
kml_path = 'test-kml.kml'


def read_exif():
    # with open(photo_path, encoding='Latin-1') as f:
    with open(photo_path, 'rb') as f:
        print(f)
        tags = exifread.process_file(f)
        print(type(tags))
        print(tags)
        pprint(tags)
        print('==========')

        for k in tags.keys():
            # if 'GPSL' in k.upper():
            #     print(k, tags[k])
            #     print(k)
            #     pprint(k)
            #     print('type:', type(tags[k]), tags[k])
            #     pprint(tags[k])
            #     print('=====')
            if 'TIME' in k.upper():
                print(k, tags[k])
                print('=====')

        lat = tags['GPS GPSLatitude']
        lat_ref = tags['GPS GPSLatitudeRef']
        long = tags['GPS GPSLongitude']
        long_ref = tags['GPS GPSLongitudeRef']
        # print(lat, lat_ref)
        # print(long, long_ref)
        # print('=====')

        # using PIL
        im = Image.open(f)
        tags_pil = im._getexif()
        # print(tags_pil)
        for tag, value in tags_pil.items():
            decoded = TAGS.get(tag, tag)
            # if decoded is 'GPSInfo':
            #     print(decoded)
            #     pprint(value)
            print(decoded)
    # image = exifgps.read(photo_path)
    # image.process_exif()
    # print(image)
    # print(image.get_url())


def write_kml():
    print('=====')
    print('===== Building KML =====')
    k = kml.KML()
    # print(k)
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns, 'docid', 'doc name', 'doc description')
    k.append(d)

    p = kml.Placemark(ns, 'id', 'name', 'description')
    # p.geometry = Polygon([(0,0,0), (1,1,0), (1,0,1)])
    easting = 128.4
    northing = 36.4
    elevation = 0  # does Google Earth show points that are under terrain or buildings?

    # KML uses long, lat, alt for ordering coordinates (x, y, z)
    p.geometry = Point(easting, northing, elevation)
    d.append(p)

    # kml.Placemark

    print(k.to_string(prettyprint=True))

    with open(kml_path, 'w') as f:
        f.write(k.to_string())

    with open(kml_path, 'r') as f:
        print(f.read())


def list_photos():
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    # print(target)
    f = []
    for (dirpath, dirnames, filesnames) in walk(target):
        # print(dirpath, dirnames, filesnames)
        # for f in filesnames:
        #     if not f.upper().endswith('.JPG') or not f.upper().endswith('.JPEG'):
        #         filesnames.remove(f)
        path_filenames = []
        for file in filesnames:
            path_filenames.append(dirpath + file)
        f.extend(path_filenames)
        break  # call to walk only the top directory
    print(f)
    print(len(f))


def main():
    # read all the EXIF data from the target folder (or webserver?)
    # generate a KML with points
    # date-time of photo
    # any other EXIF data
    # make a KMZ that includes the photos (or URL to show the photo in Google Earth)

    # 2 approaches:
    #       1. Batch process everything in phases, doing one action to all the objects
    #       2. Process each item individually through the phases. DevOps = small batch size
    # Going with option 2.

    # initialize the KML document
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns, 'docid', 'doc name', 'doc description')  # TODO update fields
    k.append(d)

    files = []
    for (dirpath, dirnames, filesnames) in walk(target):
        path_filenames = []
        for file in filesnames:
            path_filenames.append(dirpath + file)
        files.extend(path_filenames)
        break  # call to walk only the top directory

    for file in files:
        # print(file)
        # read EXIF
        # with open(file) as f:  # exifread takes filenames
        # tags = exifread.process_file(file)  # exifgps can open files also

        # convert EXIF coordinate format to KML coordinate format
        imagegps = exifgps.read(file)
        # print(imagegps)
        imagegps.process_exif()
        if imagegps._has_gps:
            print(file, imagegps._decimal_degrees)

            northing, easting = imagegps._decimal_degrees  # order is latitude, longitude
            elevation = 0

            # construct the KML tag and add it
            # TODO set the relative altitude mode...
            p = kml.Placemark(ns, file, file, file)
            # KML uses long, lat, alt for ordering coordinates (x, y, z)
            p.geometry = Point(easting, northing, elevation)
            d.append(p)
    # finish the KML
    print(k.to_string(prettyprint=True))
    with open(kml_path, 'w') as f:
        f.write(k.to_string())


read_exif()
# write_kml()
# list_photos()
# main()
