# hackers.gg
# Captcha 2
# must reply within 1000ms

# could OCR, or could build a lookup table if the chars are the same every time?

import cairosvg
import pytesseract
import requests
from PIL import Image
# from io import BytesIO
from bs4 import BeautifulSoup as bs

# download SVG
url = 'http://hackers.gg:8765/'
# r = requests.get(url).content.decode()
# print(r)
img = url + 'captcha/'
# print(img)

counter = 0
success_counter = 0
while True:
    counter += 1

    r = requests.get(img)
    r_img = r.content
    # print(type(r_img))
    # pprint(r_img)

    # (optional?) remove lines
    soup = bs(r_img.decode(), 'lxml')
    # pprint(soup)
    # remove <path fill="none">
    # print(soup.find_all('path', attrs={"fill": "none"}))
    for tag in soup.find_all('path', attrs={"fill": "none"}):
        tag.decompose()

    # pprint(soup.svg)

    for tag in soup.svg:
        # print(tag)
        tag['fill'] = 'black'
        tag['stroke'] = 'black'

    # convert to png
    png = 'captcha2_test.png'
    with open(png, 'wb+') as fout:
        # cairosvg.svg2png(bytestring=r_img, write_to=fout)
        cairosvg.svg2png(bytestring=soup.svg.encode(), write_to=fout)
        # png_bytestr = cairosvg.svg2png(bytestring=r_img)
        # print(png_bytestr)

    # OCR to text
    # text = pytesseract.image_to_string(Image.open(BytesIO(png_bytestr)))
    text = pytesseract.image_to_string(Image.open(png), lang='eng')
    text = text.replace(' ', '')
    # print(text)
    # print(type(text), len(text))

    # submit text
    # print(r.cookies)
    # print(jar)
    if text == '':
        continue
    submit = requests.get('http://hackers.gg:8765/captcha_submit?answer=' + text, cookies=r.cookies)

    # print(dir(submit))
    # print(submit.cookies)
    # print(r.cookies)
    # print(submit.content)
    if submit.content != b'YOU FAILED!' and submit.content != b'400 - U Took 2 Long':
        success_counter += 1
        print(submit.content)

        if success_counter > 10:
            print('Success: ', success_counter)
            print('Tries: ', counter)
            print('Percent Success: ', success_counter / counter * 100)
            exit()
