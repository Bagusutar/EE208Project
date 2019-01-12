# -*- coding: utf-8 -*-
import os, sys, time, random, traceback
import json, urllib2, requests, get_ip
from datetime import datetime as date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

reload(sys)
sys.setdefaultencoding("utf-8")

"""
这个文件包含爬虫模块必须的类和函数。
使用此爬虫需安装Chrome浏览器，并将压缩包中的chromedriver.exe文件放入Chrome安装目录的Application文件夹中
能实现的功能包括：
1.随机获取代理IP（可不使用）
2.初始化谷歌浏览器（需输入谷歌浏览器的路径）
3.获取网页内容（可设置访问时间限制）
4.访问iframe框架（需输入框架的name、class或id）
"""

is_proxy = 0  # 是否使用代理IP
# 代理IP地址设置
if is_proxy:
    # 读取已经获取的代理IP地址
    ip_list = []
    IP = open('IP.txt', 'a+')
    for ip in IP.readlines():
        ip_list.append(ip.strip())
    IP.close()

    # 若没有代理IP信息则创建
    if not ip_list:
        IP = open('IP.txt', 'a+')
        ip_list = get_ip.get_ip_list()
        for ip in ip_list:
            IP.write('http://' + ip + '\n')
        IP.close()


def get_random_ip():
    """
    :return: 返回随机代理IP
    """
    return random.choice(ip_list)


def init_driver(
        driver_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
        UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"):
    """
    :param driver_path: 浏览器路径
    :param UserAgent: 请求头
    :return: 浏览器对象
    """
    # 初始化无头浏览器，添加随机代理IP
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--user-agent={}".format(UserAgent))
    if is_proxy:
        chrome_options.add_argument("--proxy-server={}".format(get_random_ip()))
    chrome_driver = webdriver.Chrome(executable_path=driver_path,
                                     chrome_options=chrome_options)  # 浏览器需放在Chrome安装目录的相应文件夹中
    return chrome_driver


def page_loading_timeout(driver, url, time):
    """
    :param driver: 浏览器对象
    :param url: 访问的网页链接
    :param time: 设置超时时间，单位是秒
    :raise: 若超时则发送错误信息
    """
    driver.set_page_load_timeout(time)
    try:
        driver.get(url)  # 获取网页内容
    except Exception as e:
        # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
        driver.execute_script("window.stop()")
        raise e


def switch_to_iframe(driver, iframe):
    """
    :param driver: 浏览器对象
    :param iframe: iframe框架的name、class或id
    :raise: 若iframe框架访问失败则发送错误信息
    """
    try:
        driver.switch_to.frame(iframe)  # 跳转到iframe框架
    except Exception as e:
        raise e


def get_page(driver, url, iframe, time=6):
    """
    :param driver: 浏览器对象
    :param url: 爬取网页的链接
    :param iframe: iframe框架的name、class或id
    :param time: 爬取网页的时间上限，若超时则中止爬取
    :raise: 向调用函数的程序发送错误信息
    """
    try:
        page_loading_timeout(driver, url, time=time)
        switch_to_iframe(driver, iframe)
    except Exception as e:
        if e.__class__.__name__ == 'TimeoutException':
            raise Exception("Time out after %s seconds when loading page." % time)
        if e.__class__.__name__ == 'NoSuchFrameException':
            raise Exception("Can't switch to iframe.")
        raise e


def mkdir(path):
    """
    :param path: 若不存在该文件夹则创建
    """
    if not os.path.exists(path):
        os.mkdir(path)
