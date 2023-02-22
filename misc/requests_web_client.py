import requests
from requests.structures import CaseInsensitiveDict

url = "http://localhost:8080/math/area"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

data = "type=rectangle&width=5&height=2\n\n\n&test="


resp = requests.post(url, headers=headers, data=data)

######


req = requests.Request('POST',url, headers=headers,data=data)
prepared = req.prepare()

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(prepared)
print("-------")




print()

print(resp.status_code)
print(resp.content)

