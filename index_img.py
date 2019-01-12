#coding=utf8
import os,pprint
import cv2,time
import pickle as pk
#target="234.jpg"
import numpy as np
'''
遍历图片文件夹，得到图片的keypoint 和description
保存到 desPath 文件中
'''

#-------------算法-----------------------------
orb = cv2.ORB_create(nfeatures=300)
sift= cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
star = cv2.xfeatures2d.StarDetector_create()   #只是角点检测
brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()   #只是特征计算
fast = cv2.FastFeatureDetector_create()   #只是角点检测
method = orb
#--------------------------------------------
dir="./static/Image"                 #保存图片的文件夹
desPath="./static/img_des.pkl"         #保存图片orb 特征的文件
#--------------------------------------------

desdic={}
now=0
for i in os.listdir(dir):
    print "processing"+str(now)
    now+=1

    path=os.path.join(dir,i)
    try:
        if (os.path.isfile(path) and path.endswith(".jpg")):
            img=cv2.imread(path,0)

            kp,des=method.detectAndCompute(img,None)
            if len(kp)==0:
                continue
            else:
                desdic[path]=des
    except Exception,e:
        print Exception
        continue

file=open(desPath,"wb")
pk.dump(desdic,file)
file.close()



"""

def Com(x,y):

    if x[0]>y[0]:
        return -1
    if x[0]==y[0] and x[1]<y[1]:
        return -1
    return 1


f = open("img_des2.pkl", "rb")
data= pk.load(f)
f.close()
start=time.clock()
target_color = cv2.imread(target, cv2.IMREAD_COLOR)
target_gray = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
orb = cv2.ORB_create(nfeatures=300)
method = orb
kp,des=method.detectAndCompute(target_gray,None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
Max=0
pipei=" "

now=0
Result=[]

for k,v in data.items():
    now+=1

    matches = bf.match(des,v)
    Sum=0
    Total=0
    #matches = sorted(matches, key = lambda x:x.distance)
    for i in range(len(matches)):
        if matches[i].distance<50:
            Sum+=1
            Total+=matches[i].distance

    if Sum!=0:
        Result.append([Sum,Total,k])

print len(Result)
Result.sort(Com)
print Result
print time.clock()-start

pipei=Result[0][2]
img1=cv2.imread(target, 1)
img2=cv2.imread(pipei, 1)

Max=max(img1.shape[0],img1.shape[1])
if (Max>800):
    size=800.0/float(Max)
    img1=cv2.resize(img1, (0,0), fx=size, fy=size)
Max=max(img2.shape[0],img2.shape[1])
if (Max>800):
    size=800.0/float(Max)
    img2=cv2.resize(img2, (0,0), fx=size, fy=size)
rows1 = img1.shape[0]  # 获取两幅图的尺寸
cols1 = img1.shape[1]
rows2 = img2.shape[0]
cols2 = img2.shape[1]
Merge = np.zeros((max([rows1, rows2]), cols1 + cols2, 3), dtype='uint8')  # 设置可以容纳两幅图的矩阵
Merge[:rows1, :cols1, :] = np.array(img1)  # 左边是目标图像
Merge[:rows2, cols1:cols1 + cols2, :] = np.array(img2)  # 右边是最匹配的图像

cv2.imshow('Match', Merge)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Draw first 10 matches.


"""


