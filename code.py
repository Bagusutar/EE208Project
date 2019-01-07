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
    '/s', 'text',
    '/i', 'image'
)

render = web.template.render('templates')


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


class image:


    def POST(self):
        user_data = web.input()
        print user_data.keys()
        if (len(user_data['myfile'])>0):

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
                return render.formtest_img()
        if (len(user_data['search_content']) > 0):

            user_data = web.input(search_content=None)
            term = str(user_data.search_content)
            if not term:
                return render.formtest()
            if term in song_information:
                print "song_information"+"  "+term
            else:
                if term in artist_information:
                    print "artist_information" + "  " + term
                else:
                    if term in album_information:
                        print "album_information" + "  " + term
            #contents, num = search(term)
            #return render.result(term, contents, num)

if __name__ == "__main__":
    app = web.application(urls, globals(), False)
    app.run()
