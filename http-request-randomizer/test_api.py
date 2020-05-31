import time
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print("Initialization took: {0} sec".format((time.time() - start)))
    print("Size: {0}".format(len(req_proxy.get_proxy_list())))
    print("ALL = {0} ".format(list(map(lambda x: x.get_address(), req_proxy.get_proxy_list()))))

    test_url = 'http://ipv4.icanhazip.com'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print("Proxied Request Took: {0} sec => Status: {1}".format((time.time() - start), request.__str__()))
        if request is not None:
            print("\t Response: ip={0}".format(u''.join(request.text).encode('utf-8')))
        print("Proxy List Size: {0}".format(len(req_proxy.get_proxy_list())))

        print("-> Going to sleep..")
        time.sleep(10)
