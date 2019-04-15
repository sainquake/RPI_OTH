#!/usr/bin/env python3
import requests
r = requests.get("127.0.0.1:8080/hello?tx=123")
print(r)