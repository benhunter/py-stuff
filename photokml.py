# PhotoKML
# Use geo-tagged photos to build a Google Earth file showing the photos where they were taken. Uses EXIF data to generate a KML.
# TODO Add web photo album enumeration: Google Drive, Google Photos, Instagram (EXIF?), Imgur (EXIF?)
# TODO GUI...

# https://github.com/collective/collective.geo.exif/blob/master/collective/geo/exif/readexif.py
# KML Docs: https://developers.google.com/kml/documentation/kml_tut
# KML Schema: http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd
# KML Sample: https://developers.google.com/kml/documentation/KML_Samples.kml


import os
import sys
from os import walk

import exifgps  # WARNING!!! NOT Python 3 ready (uses print statement)
# Use this repo until exifgps is updated: https://github.com/benhunter/exifgps
from fastkml import kml  # seems more current than pyKML
from shapely.geometry import Point


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
    try:
        dt = self._tags['Image DateTime']
    except KeyError:
        dt = None
    return dt


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    # https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
    """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """

    # fix for finishing at 99%:
    iteration += 1

    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def main(target, outname=None, recursive=False):
    # read all the EXIF data from the target folder (or webserver?)
    # generate a KML with points
    # date-time of photo
    # any other EXIF data
    # make a KMZ that includes the photos (or URL to show the photo in Google Earth)

    exifcount = 0  # How many photos with geo EXIF data were processed.

    # TODO why don't relative paths work? Not expanded by shell?
    # TODO test cross platform paths ('\' vs '/')

    target = target.replace('/', '\\')
    target = target.strip('"')
    # fix path string on linux
    if not target.endswith('\\'):
        target += '\\'

    name = target.split('\\')[-2]
    if outname is None:
        outname = name + '.kml'

    # initialize the KML document
    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'
    d = kml.Document(ns, name, name, name)  # TODO update fields
    k.append(d)

    # Gather all the filenames in the target directory. Not recursive.
    files = []
    # TODO Note that walk() generates paths with backslashes 'dir1\\dir2'. Is this the same on linux?
    for (dirpath, dirnames, filesnames) in walk(target):
        path_filenames = []
        for file in filesnames:
            fullpath = dirpath + '\\' + file
            print(fullpath)
            path_filenames.append(fullpath)  # use the full path to each file
        files.extend(path_filenames)
        if not recursive:
            break  # call to walk only the top directory

    # order the files by name
    files.sort()

    for i, file in enumerate(files):
        imagegps = exifgps.read(file)  # create the ImageGPS object
        # print(imagegps)

        # Dynamic update to Imagegps class. Modifying _read_exif() and adding get_datetime().
        exifgps.Imagegps._read_exif = _read_exif
        exifgps.Imagegps.get_datetime = get_datetime

        try:
            imagegps.process_exif()  # read EXIF data and convert to KML coordinate format
        except:
            print('Exception while processing: ' + str(file))
            continue
        if imagegps._has_gps:
            # print(file, imagegps._decimal_degrees)

            northing, easting = imagegps._decimal_degrees  # order is latitude, longitude
            elevation = 0

            # construct the KML tag and add it
            # TODO set the relative altitude mode...
            # add '/' for Windows local paths
            if not file.startswith('\\'):
                link = 'file://\\' + file  # TODO works on Windows, test Linux
            else:
                link = 'file://' + file

            description = '<img style="max-width:500px;" src="' + \
                          link + \
                          '">'
            dt = imagegps.get_datetime()
            if dt:
                description += 'Photo taken at: ' + str(dt) + '<br>'
            description += '<a href="' + file + '">' + file + '</a>'

            p = kml.Placemark(ns, file, file.split('\\')[-1], description)
            # KML uses long, lat, alt for ordering coordinates (x, y, z)
            p.geometry = Point(easting, northing, elevation)
            d.append(p)
            exifcount += 1
            print_progress(i, len(files), bar_length=50)

    print('Found', exifcount, 'geo-tagged photos.')
    # finish the KML
    # print(k.to_string(prettyprint=True))

    if exifcount == 0:
        print('Exiting...')
        return

    with open(outname, 'w') as f:
        f.write(k.to_string())
        print('Finished. Wrote output to:', outname)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error! No path specified.')
        print('Usage: %s <path> [output] [-r]' % sys.argv[0])
        exit()
    print('Running PhotoKML.')
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], recursive=True)
    else:
        main(sys.argv[1])
