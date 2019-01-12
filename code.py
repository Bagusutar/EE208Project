# -*- coding:utf-8 -*-
import web,os,pickle as pk
from SearchFiles import search
from SearchPics import Search_img

f = open("./static/img_des.pkl", "rb")
img_data = pk.load(f)
f.close()
f=open("./static/album.pkl","rb")
album_data = pk.load(f)
f.close()
f=open("./static/album_information.pkl","rb")
album_information= pk.load(f)
f.close()
f=open("./static/song_information.pkl","rb")
song_information= pk.load(f)
f.close()
f=open("./static/artist_information.pkl","rb")
artist_information= pk.load(f)
f.close()

urls = (
    '/', 'index',
    '/im', 'index_img',
    '/s_song', 'song',
    '/s_art','artist',
    '/s_alb','album',
    '/i', 'image',
'/test1', 'test1',
'/test2','test2'
)

render = web.template.render('templates')


class test2:
    def GET(self):
        print 5
        user_data=web.input()
        filename=str(user_data['img_name'])
        filepath = './static/Query/' + (filename.replace('\\', '/'))
        filepath, target, num = Search_img(filepath, img_data, album_data)

        return render.result_img(filepath, target, num)


class test1:
    def POST(self):
        print 6
        user_data=web.input()
        image_inputs = web.input(imgup={})
        filename = str(image_inputs.imgup.filename)

        k = filename.split('.')

        if 'jpg' in k:
            filepath = './static/Query/' + (filename.replace('\\', '/'))  # 问题：文件名中存在路径分隔符？

            fout = open(filepath, 'wb')

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
        root = "music"
        if not term:
            return render.formtest()
        contents, num = search(root,term)

        for i in range(len(contents)):
            contents[i].append("./static/Music/"+str(contents[i][0])+".mp3")

            lyrics = contents[i][8].split('\n')
            lyrics = filter(isspace, lyrics)
            contents[i][8] = lyrics
        return render.music(term, contents, num)


class artist:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        root = "artist"
        if not term:
            return render.formtest()
        contents, num = search(root,term)
        return render.artist(term, contents, num)


class album:
    def GET(self):
        user_data = web.input(search_content=None)
        term = user_data.search_content
        root = 'album'
        if not term:
            return render.formtest()
        contents, num = search(root,term)
        return render.album(term, contents, num)


class image:
    def POST(self):
        user_data = web.input()
        print user_data.keys()
        if len(user_data['myfile'])>0:
            image_inputs = web.input(myfile={})
            filename = image_inputs.myfile.filename
            k=filename.split('.')
            print k
            if 'jpg' in k :
                filepath ='./static/Query/'+(filename.replace('\\', '/'))  # 问题：文件名中存在路径分隔符？
                fout = open(filepath, 'wb')
                fout.write(image_inputs.myfile.value)
                fout.close()
                filepath,target,num=Search_img(filepath,img_data,album_data)
                return render.result_img(filepath,target,num)
            else :
                return render.formtest()

        if len(user_data['search_content']) > 0:
            user_data = web.input(search_content=None)
            term = str(user_data.search_content)
            if not term:
                return render.formtest()
            if term in artist_information:
                root = "artist"
                contents, num = search(root, term)
                print "artist_information" + "  " + term
                return render.artist(term, contents, num)
            else:
                if term in album_information:
                    print "album_information" + "  " + term
                    root = 'album'
                    contents, num = search(root, term)
                    return render.album(term, contents, num)
                else:
                    root = "music"
                    contents, num = search(root, term)
                    for i in range(len(contents)):
                        contents[i].append("./static/Music/" + str(contents[i][0]) + ".mp3")
                        lyrics = contents[i][8].split('\n')
                        lyrics=filter(isspace,lyrics)
                        contents[i][8] = lyrics
                    return render.music(term, contents, num)


def isspace(x):
    return x.isspace()==False and x!=''


if __name__ == "__main__":
    app = web.application(urls, globals(), False)
    app.run()
