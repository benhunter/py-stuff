import ipaddress

ip_list = '''1.1.1.1,1.1.1.0/24
192.168.0.75,10.10.10.0/24
192.31.199.233,126.175.187.164/31
192.88.97.247,115.108.0.0/14
198.51.56.59,192.175.61.144/29
192.31.218.80,164.175.96.0/19
203.0.120.150,198.10.96.128/27'''

ip_list = ip_list.splitlines()

for pair in ip_list:
    ip, subnet = pair.split(',')
    print(ipaddress.ip_address(ip) in ipaddress.ip_network(subnet).hosts())
