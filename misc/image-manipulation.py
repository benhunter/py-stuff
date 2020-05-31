from io import BytesIO

import requests
from PIL import Image

link = 'https://i.redditmedia.com/f37uSbF_Y7ssvV7__Z9PJSj4ULoCojmli1cmDXCbyss.jpg?s=d02e01567d6a0541b3e88fc007176203'

req = requests.get(link)
im = Image.open(BytesIO(req.content))
print(im)

im.show()
