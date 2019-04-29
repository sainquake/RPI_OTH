#!/usr/bin/env python
#Released under CC0
import requesocks
#Initialize a new wrapped requests object
session = requesocks.session()
#Use Tor for both HTTP and HTTPS
session.proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
#fetch a page that shows your IP address
response = session.get('http://httpbin.org/ip')
print(response.text)

