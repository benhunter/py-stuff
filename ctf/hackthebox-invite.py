import base64
import json
import requests

# deobfustace the javascript
# rot13 the message

url = 'https://www.hackthebox.eu/api/invite/generate'

code = requests.post(url)
print(code.content)

data_dict = json.loads(code.content)
b64_encoded = data_dict['data']['code']
print(b64_encoded)

print(base64.b64decode(b64_encoded))
