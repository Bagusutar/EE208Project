# -*- coding: utf-8 -*-
from CrawlerSetting import *

"""
这个文件是用来爬取网易云歌单中的歌曲的其他信息并保存的。获取信息如下：
1.歌曲歌词 2.歌手图片 3.专辑图片
保存文件格式如下：
music文件夹：
  一.歌曲ID文件：保存已经爬取的歌曲ID
  二.歌曲信息文件：1.歌曲链接 2.歌曲名 3.歌手链接 4.歌手名 5.专辑链接 6.专辑名 7.专辑图片 8.歌词
album文件夹：
  一.专辑图片（130x130）
  二.专辑信息文件：1.专辑ID 2.专辑名 3.专辑链接 4.歌手名 5.歌手链接 7.专辑图片
artist文件夹：
  一.歌手图片（640x300）
  二.歌手信息文件：1.歌手ID 2.歌手名 3.歌手图片
"""

# 创建文件夹
mkdir('music')
mkdir('album')
mkdir('artist')

# 读取已经爬取的歌曲、专辑、歌手ID
crawled_songs = []
crawled_albums = []
crawled_artists = []

music = open('music/music.txt', 'a+')
album = open('album/album.txt', 'a+')
artist = open("artist/artist.txt", 'a+')

for line in music.readlines():
    line = line.strip()
    crawled_songs.append(line)

for line in album.readlines():
    line = line.strip()
    crawled_albums.append(line[:line.find('\t')])

for line in artist.readlines():
    line = line.strip()
    crawled_artists.append(line[:line.find('\t')])

music.close()
album.close()
artist.close()

# 读取待爬取歌曲信息文件
musics = []  # 保存待爬取歌曲信息
music = open('music.txt', 'r')
for line in music.readlines():
    line = line.strip()
    line = line.split('\t')
    if line[0] not in crawled_songs:
        musics.append(line)
music.close()

# 初始化参数
maxSong = 5000  # 最大爬取的歌曲数
n = 0  # 已经爬取的歌曲数
wrong = 0  # 当前已经发生的错误数

# 初始化浏览器
driver = init_driver()

print "Start:"

while n < min(len(musics), maxSong - len(crawled_songs)):
    try:
        # 获取歌曲信息
        song_id, song_link, song_name, artist_link, artist_name, album_link, album_name = musics[n]

        # 写入文件的内容
        album_content = ''
        album_img_link = ''
        album_img_content = ''
        artist_content = ''
        artist_img_link = ''
        artist_img_content = ''

        # 是否是新专辑和歌手
        new_album = False
        new_artist = False

        try:
            time.sleep(1)  # 减慢爬虫速度，减小服务器负担，避免IP被封禁
            get_page(driver, song_link, "contentFrame")
            wrong = 0
        except Exception as e:
            # 计录出错次数，若连续出错超过10次，则重启浏览器
            wrong += 1
            print wrong, e, date.now()
            if wrong >= 5:
                print "Got wrong too many times, reset the driver...", date.now(), '\n'
                driver.quit()
                driver = init_driver()
                wrong = 0
            continue

        # ------------------获取专辑图片------------------
        album_id = album_link[album_link.find('id=') + 3:]
        if album_id not in crawled_albums:
            album_img_link = driver.find_element_by_class_name("j-img") \
                .get_attribute("src")
            req = urllib2.Request(album_img_link, None, {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome' +
                              '/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2767.400'})
            album_img_content = urllib2.urlopen(req, timeout=1)
            album_content = album_id + '\t' + album_name + '\t' + album_link + '\t' + artist_name + '\t' + \
                            artist_link + '\t' + album_img_link + '\n'
            if not album_img_content:
                musics.remove(musics[n])
                continue
            new_album = True

        # ------------------获取歌手图片------------------
        artist_id = artist_link[artist_link.find('id=') + 3:]
        if artist_id not in crawled_artists:
            try:
                time.sleep(1)  # 减慢爬虫速度，减小服务器负担，避免IP被封禁
                get_page(driver, artist_link, "contentFrame")
                wrong = 0
            except Exception as e:
                # 计录出错次数，若连续出错超过10次，则重启浏览器
                wrong += 1
                print wrong, e, date.now()
                if wrong >= 5:
                    print "Got wrong too many times, reset the driver...", date.now(), '\n'
                    driver.quit()
                    driver = init_driver()
                    wrong = 0
                continue

            artist_img_link = driver.find_element_by_class_name("g-wrap6").find_element_by_tag_name("img") \
                .get_attribute("src")
            req = urllib2.Request(artist_img_link, None, {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome' +
                              '/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2767.400'})
            artist_img_content = urllib2.urlopen(req, timeout=1)
            artist_content = artist_id + '\t' + artist_name + '\t' + artist_img_link + '\n'
            if not artist_img_content:
                musics.remove(musics[n])
                continue
            new_artist = True

        # --------------------获取歌词--------------------
        lyric_url = 'http://music.163.com/api/song/lyric?id=' + song_id + '&lv=1&kv=1&tv=-1'  # 网易云保存歌词的链接
        r = requests.get(lyric_url)
        json_obj = r.text
        j = json.loads(json_obj)
        try:
            lyric_lines = j['lrc']['lyric'].split('\n')
            lyrics = ''
            for lyric_line in lyric_lines:
                if ']' in lyric_line:
                    lyrics += (lyric_line.split(']')[-1] + '\n')
        except:
            lyrics = '无歌词'
        music_content = song_link + '\n' + song_name + '\n\n' + artist_link + '\n' + artist_name + '\n\n' \
                        + album_link + '\n' + album_name + '\n\n' + album_img_link + '\n\n' + lyrics

        # 保存专辑信息
        if new_album:
            img = open('album/' + album_id + ".jpg", 'wb')
            img.write(album_img_content.read())
            img.close()
            album = open('album/album.txt', 'a')
            album.write(album_content)
            album.close()
            crawled_albums.append(album_id)

        # 保存歌手信息
        if new_artist:
            img = open('artist/' + artist_id + ".jpg", 'wb')
            img.write(artist_img_content.read())
            img.close()
            artist = open("artist/artist.txt", 'a')
            artist.write(artist_content)
            artist.close()
            crawled_artists.append(artist_id)

        # 保存歌曲信息
        music_file = open('music/' + song_id + '.txt', 'w')
        music_file.write(music_content)
        music_file.close()
        music = open('music/music.txt', 'a+')
        music.write(song_id + '\n')
        music.close()

        n += 1
        print '*', n, song_name, date.now()

    except:
        print traceback.format_exc()
        musics.remove(musics[n])
        continue

driver.quit()  # 清除浏览器缓存
print "Complete"
