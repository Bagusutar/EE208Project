# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

"""
这个文件是用来获取一定数量的IP地址并写入到文本文件中的
"""


def get_ip_list(max_num=100):
    # 获取一个IP池
    seed = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    page = 0
    num = 0
    ip_list = []
    while num < max_num:
        if page == 0:
            url = seed
        else:
            url = seed + str(page)
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        ips = soup.find_all('tr')
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            speed = float(tds[6].find('div').get('title')[:-1])
            if speed < 0.5:
                ip_list.append(tds[1].text + ':' + tds[2].text)
                num += 1
                if num >= max_num:
                    break
        page += 1
    return ip_list
