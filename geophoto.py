# import exifgps
from pprint import pprint

import exifread

photo_path = 'E:\\google drive\\Photos and Videos\\Class River\\IMG_1406.JPG'

# with open(photo_path, encoding='Latin-1') as f:
with open(photo_path, 'rb') as f:
    print(f)
    tags = exifread.process_file(f)
    print(type(tags))
    print(tags)
    pprint(tags)
    print('=====')

    for k in tags.keys():
        if 'GPSL' in k.upper():
            print(k, tags[k])
            print(k)
            pprint(k)
            print('type:', type(tags[k]), tags[k])
            pprint(tags[k])
            print('=====')

# image = exifgps.read(photo_path)
# image.process_exif()
# print(image)
# print(image.get_url())
