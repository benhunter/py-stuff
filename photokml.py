# Use geo-tagged photos to build a Google Earth file showing the photos where they were taken. Uses EXIF data to generate a KML.
# TODO Add web photo album enumeration: Google Drive, Google Photos, Instagram (EXIF?), Imgur (EXIF?)

# https://github.com/collective/collective.geo.exif/blob/master/collective/geo/exif/readexif.py
# KML Docs: https://developers.google.com/kml/documentation/kml_tut
# KML Schema: http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd
# KML Sample: https://developers.google.com/kml/documentation/KML_Samples.kml


import os
import sys
from os import walk

import exifgps  # NOT Python 3 ready (uses print statement)
from fastkml import kml  # seems more current than pyKML
from shapely.geometry import Point

OUTNAME = 'photos.kml'


def _read_exif(self, filename):
    '''
    Dynamic update to Imagegps in exifgps/__init__.py
    Stores all the EXIF tags in the Imagegps object
    '''
    gps = {}

    if os.path.exists(filename) == False:
        print("Error: Unable to open %s" % filename)
        return None

    with open(filename, "rb") as fh:
        import exifread  # added
        tags = exifread.process_file(fh, details=False)
        self._tags = tags  # the new code so tags are accessible

    if len(tags) != 0:
        for tag in tags.keys():
            if "GPS" in tag:
                gps[tag] = tags[tag]
    return gps


def get_datetime(self):
    '''
    Dynamic update to Imagegps in exifgps/__init__.py
    Retrieves the DateTime EXIF tag.
    '''
    return self._tags['Image DateTime']


def main(target, outname=OUTNAME, recursive=False):
    # read all the EXIF data from the target folder (or webserver?)
    # generate a KML with points
    # date-time of photo
    # any other EXIF data
    # make a KMZ that includes the photos (or URL to show the photo in Google Earth)

    exifcount = 0  # How many photos with geo EXIF data were processed.

    # TODO why don't relative paths work? Not expanded by shell?
    # TODO test cross platform paths ('\' vs '/')
    # fix path string on linux
    if not target.endswith('/'):
        target += '/'

    # initialize the KML document
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns, 'docid', 'doc name', 'doc description')  # TODO update fields
    k.append(d)

    # Gather all the filenames in the target directory. Not recursive.
    files = []
    for (dirpath, dirnames, filesnames) in walk(target):
        path_filenames = []
        for file in filesnames:
            path_filenames.append(dirpath + file)  # use the full path to each file
        files.extend(path_filenames)
        if not recursive:
            break  # call to walk only the top directory

    # order the files by name
    files.sort()

    for file in files:
        imagegps = exifgps.read(file)  # create the ImageGPS object
        # print(imagegps)

        # Dynamic update to Imagegps class. Modifying _read_exif() and adding get_datetime().
        exifgps.Imagegps._read_exif = _read_exif
        exifgps.Imagegps.get_datetime = get_datetime

        imagegps.process_exif()  # read EXIF data and convert to KML coordinate format
        if imagegps._has_gps:
            # print(file, imagegps._decimal_degrees)

            northing, easting = imagegps._decimal_degrees  # order is latitude, longitude
            elevation = 0

            # construct the KML tag and add it
            # TODO set the relative altitude mode...
            description = 'Photo taken at: ' + str(
                imagegps.get_datetime()) + '<img style="max-width:500px;" src="file://' + file + '">' + file
            p = kml.Placemark(ns, file, file.split('/')[-1], description)
            # KML uses long, lat, alt for ordering coordinates (x, y, z)
            p.geometry = Point(easting, northing, elevation)
            d.append(p)
            exifcount += 1

    print('Found', exifcount, 'geo-tagged photos.')
    # finish the KML
    # print(k.to_string(prettyprint=True))
    with open(outname, 'w') as f:
        f.write(k.to_string())
        print('Finished. Wrote output to:', outname)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error! No path specified.')
        print('Usage: %s <path> [output]' % sys.argv[0])
        exit()
    print('Running PhotoKML.')
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])
