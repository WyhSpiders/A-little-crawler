# -*- coding: utf-8 -*-

'''
Info
- author : "wyh"
- date   : "2018.3.21"
- description : 下载网页源代码
'''
import requests
import random
from tomorrow import threads
import time

PROXY_POOL_URL = 'http://localhost:5555/random'
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    #"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Host": "www.zhihu.com",
        #"Referer": "https://www.zhihu.com/"
}


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            proxy = response.text
            proxies = {'https': 'https://' + proxy}
			return proxies
    except ConnectionError:
        return None

@threads(10)
def get_page(url, headers=headers):
    try:
        response = requests.get(url, headers=headers, proxies=get_proxy(), timeout=10)
        print('正在下载页面{}...'.format(url))
        time.sleep(random.uniform(0,3))
    except:
        get_page(url)
    return response