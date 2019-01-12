# -*- coding: utf-8 -*-
from CrawlerSetting import *

"""
这个文件是用来爬取网易云歌单的。流程如下：
1.爬取歌单当前页中的歌单链接
2.获取下一页歌单链接并跳转
3.重复步骤1，直到下一页链接为空
"""

# 读取已经爬取的歌单链接文件
playlists = []  # 保存已经爬取的歌单链接
playlist = open("playlist.txt", "a+")

for line in playlist.readlines():
    playlists.append(line.strip())

playlist.close()

# 初始化参数
url = 'https://music.163.com/#/discover/playlist'  # 网易云歌单首页
startPage = 1  # 从哪一页开始爬取
endPage = 1000  # 爬取到哪一页停止
P = startPage  # 当前页页码
maxNum = 0  # 最大爬取的歌单数
currentNum = len(playlists)  # 当前的歌单数

# 初始化浏览器
driver = init_driver()

print "Start:"

while url != 'javascript:void(0)':
    try:
        if P > endPage:
            break
        try:
            get_page(driver, playlist, iframe='contentFrame')  # 获取链接
        except Exception as e:  # 若访问失败，重启浏览器
            print e, "Restart the driver...\n"
            driver.quit()
            driver = init_driver()
            continue

        if P >= startPage:
            print 'P' + str(P)
            data = driver.find_element_by_id("m-pl-container").find_elements_by_tag_name("li")  # 定位所有存在歌单链接的框架
            playlist = open("playlist.txt", "a+")
            for d in data:
                link = d.find_element_by_class_name('msk').get_attribute('href')  # 定位存放歌单链接的元素并获取链接
                if link and link not in playlists:
                    playlists.append(link)
                    playlist.write(link + '\n')  # 将链接写入文件
                    currentNum += 1
                    print '&', currentNum, link
            playlist.close()

        url = driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute("href")  # 获取下一页链接
        P += 1
    except Exception as e:
        print e
        continue

driver.quit()
print "Complete"
