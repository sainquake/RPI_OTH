# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import requests  
import datetime

# NOTE: tor должен быть запущен
# pip3 install -U requests[socks]
# pip3 install 'urllib3[socks]'
# pip3 install pysocks
# pip3 install requests[socks]
# https://api.telegram.org/bot330036157:AAHVdF7NL_uvDVPM9E1w4CS67uRheme65QA/getUpdates
proxies = {
    'http': 'socks5://localhost:9040',
    'https': 'socks5://localhost:9040'
}

url = 'http://httpbin.org/ip'
print(requests.get(url, proxies=proxies).text)

#print(requests.get(url, proxies=proxies).text)

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params,proxies=proxies)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update
		
#resp = requests.get("http://google.com")
#print( str(resp.text) )
		
		
#bot = BotHandler("330036157:AAHVdF7NL_uvDVPM9E1w4CS67uRheme65QA")  
#print( bot.get_updates() )