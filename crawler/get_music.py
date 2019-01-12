# -*- coding: utf-8 -*-
from CrawlerSetting import *

"""
这个文件是用来爬取网易云歌单中的歌曲的。获取信息如下：
1.歌曲ID 2.歌曲链接 3.歌曲名 4.歌手链接 5.歌手名 6.专辑链接 7.专辑名
"""

# 读取已经爬取的歌曲信息文件
crawled_songs = []  # 保存已经爬取的歌曲信息
musics = open('music.txt', 'a+')

for line in musics.readlines():
    line = line.strip()
    crawled_songs.append(line[:line.find('\t')])

musics.close()

# 读取待爬取歌单链接文件
playlists = []  # 保存待爬取歌单链接
playlist = open('playlist.txt', 'a+')
for line in playlist.readlines():
    playlists.append(line.strip())
playlist.close()

# 初始化参数
L = 1  # 当前歌单序号
N = len(crawled_songs)  # 已经爬取的歌曲数
maxSong = 50000  # 最大爬取的歌曲数

# 初始化浏览器
driver = init_driver()

print "Start:"

while N < maxSong:
    playlist = playlists[L - 1]
    print 'L' + str(L)

    try:
        time.sleep(1)  # 减慢爬虫速度，减小服务器负担，避免IP被封禁
        get_page(driver, playlist, iframe='contentFrame')  # 获取链接
    except Exception as e:  # 若访问失败，重启浏览器
        print e, "Restart the driver...\n"
        driver.quit()
        driver = init_driver()
        continue

    try:
        data = driver.find_element_by_id("song-list-pre-cache") \
            .find_element_by_tag_name("tbody") \
            .find_elements_by_tag_name("tr")  # 获取所有歌曲信息
    except Exception as e:
        print e
        L += 1
        continue

    for d in data:
        try:
            # 每首歌所在的表格
            form = d.find_elements_by_tag_name("td")

            # 音乐标签
            song_tag = form[1].find_element_by_tag_name("a")
            song_link = song_tag.get_attribute('href')
            song_id = song_link.split('id=')[1]
            if song_id in crawled_songs:
                continue
            song_name = song_tag.find_element_by_tag_name("b").get_attribute('title')

            # 歌手标签
            artist_tag = form[3].find_element_by_tag_name("span")
            artist_link = artist_tag.find_element_by_tag_name("a").get_attribute('href')
            artist_name = artist_tag.get_attribute('title')

            # 专辑标签
            album_tag = form[4].find_element_by_tag_name("a")
            album_link = album_tag.get_attribute('href')
            album_name = album_tag.get_attribute('title')

            # 保存歌曲信息
            if song_link and song_name and artist_link and artist_name and album_link and album_name:
                crawled_songs.append(song_id)
                musics = open('music.txt', 'a+')
                musics.write(
                    song_id + '\t' + song_link + '\t' + song_name + '\t' + artist_link + '\t' + artist_name + '\t' + album_link + '\t' + album_name + '\n')
                musics.close()
                N += 1
                print '#', N, song_name
                if N >= maxSong:
                    break

        except:
            print traceback.format_exc()
            continue
    L += 1

driver.quit()
print 'Complete'
