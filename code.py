# -*- coding:utf-8 -*-
import web,os,pickle as pk
from SearchFiles import search #文本检索
from SearchPics import Search_img #以图搜图
from audio import search_audio #听歌识曲

f = open("./static/img_des.pkl", "rb") #本地专辑图片ORB描述子
img_data = pk.load(f)
f.close()
f=open("./static/album.pkl","rb") #本地专辑的详细信息
album_data = pk.load(f)
f.close()
f=open("./static/album_information.pkl","rb") #专辑名
album_information= pk.load(f)
f.close()
f=open("./static/song_information.pkl","rb") #歌曲名
song_information= pk.load(f)
f.close()
f=open("./static/artist_information.pkl","rb") #歌手名
artist_information= pk.load(f)
f.close()
f=open('./static/audio_index.pkl', 'rb')
audio_index= pk.load(f)
f.close()

urls = (
    '/', 'index',
    '/im', 'index_img',
    '/s_song', 'song',
    '/s_art','artist',
    '/s_alb','album',
    '/s_ly','lyrics',
    '/i', 'image',
    '/test1', 'drag',
    '/test2','drag_search'
)

render = web.template.render('templates')


class drag_search:
    def GET(self):
        user_data=web.input()
        filename=str(user_data['img_name']) #获取上传文件名
        filepath = './static/Query/' + (filename.replace('\\', '/')) #写入路径
        if 'jpg' in filepath: #上传的是图片
            filepath, target, num = Search_img(filepath, img_data, album_data) #以图搜图
            return render.result_img(filepath, target, num) #返回结果页面
        if 'wav' in filepath: #上传的是音乐
            target = search_audio(filepath, audio_index)[0][0][0] #听歌识曲
            target = target.split('.')[0]
            return render.formtest2(filepath, target) #返回结果页面


class drag:
    def POST(self):
        user_data=web.input()
        image_inputs = web.input(imgup={})
        filename = str(image_inputs.imgup.filename) #获取文件名
        k = filename.split('.')
        if 'jpg' or 'wav' in k: #如果是图片或音频
            filepath = './static/Query/' + (filename.replace('\\', '/'))  # 写入路径
            fout = open(filepath, 'wb') #写入
            fout.write(image_inputs.imgup.value)
            fout.close()


class index:
    def GET(self):
        return render.formtest()


class index_img:
    def GET(self):
        return render.formtest_img()


class text:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        if not term:
            return render.formtest()
        contents, num = search(term)
        return render.result(term, contents, num)


class song:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        root = "music" #通过歌曲名搜索
        if not term:
            return render.formtest()
        contents, num = search(root,term)  #搜索

        for i in range(len(contents)): #设置传给网页的数据
            contents[i].append("./static/Music/"+str(contents[i][0])+".mp3")
            lyrics = contents[i][7].split('\n')
            lyrics = filter(isspace, lyrics)
            contents[i][7] = lyrics
        return render.music(term, contents, num)


class lyrics:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        root = "lyrics" #通过歌词搜索
        if not term:
            return render.formtest()
        contents, num = search(root,term) #搜索

        for i in range(len(contents)): #设置传给网页的数据
            contents[i].append("./static/Music/"+str(contents[i][0])+".mp3")
            lyrics = contents[i][7].split('\n')
            lyrics = filter(isspace, lyrics)
            contents[i][7] = lyrics
        return render.lyrics(term, contents, num)


class artist:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        root = "artist" #通过歌手名搜索
        if not term:
            return render.formtest()
        contents, num = search(root,term) #搜索
        return render.artist(term, contents, num)


class album:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        root = 'album' #通过专辑名搜索
        if not term:
            return render.formtest()
        contents, num = search(root,term) #搜索
        return render.album(term, contents, num)


class image:
    def POST(self):
        user_data = web.input()
        if len(user_data['myfile'])>0: #如果上传了文件
            image_inputs = web.input(myfile={})
            filename = image_inputs.myfile.filename #文件名
            k=filename.split('.')
            if 'jpg' in k : #上传的是图片
                filepath ='./static/Query/'+(filename.replace('\\', '/'))  # 写入路径
                fout = open(filepath, 'wb') #写入
                fout.write(image_inputs.myfile.value)
                fout.close()
                filepath,target,num=Search_img(filepath,img_data,album_data) #以图搜图
                return render.result_img(filepath,target,num)
            if 'wav' in k: #上传的是音乐
                filepath = './static/Query/' + (filename.replace('\\', '/'))  # 写入路径
                fout = open(filepath, 'wb') #写入
                fout.write(image_inputs.myfile.value)
                fout.close()
                target = search_audio(filepath, audio_index)[0][0][0] #听歌识曲
                target = target.split('.')[0]
                return render.formtest2(filepath,target)

        if (len(user_data['search_content']) > 0): #如果上传的是文本
            user_data = web.input(search_content=None)
            term = str(user_data.search_content)
            if not term:
                return render.formtest()
            if term in artist_information: #文本确定是歌手名
                root = "artist"
                contents, num = search(root, term)
                return render.artist(term, contents, num)
            else:
                if term in album_information: #文本确定是专辑名
                    root = 'album'
                    contents, num = search(root, term)
                    return render.album(term, contents, num)
                else: #不然，默认以歌名进行搜索
                    root = "music"
                    contents, num = search(root, term)
                    for i in range(len(contents)):
                        contents[i].append("./static/Music/" + str(contents[i][0]) + ".mp3")
                        lyrics = contents[i][7].split('\n')
                        lyrics=filter(isspace,lyrics)
                        contents[i][7] = lyrics
                    return render.music(term, contents, num)


def isspace(x):
    return x.isspace()==False and x!='' #过滤空格和空字符


if __name__ == "__main__":
    app = web.application(urls, globals(), False)
    app.run()
