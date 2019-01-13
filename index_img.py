#coding=utf8
import os,pprint
import cv2,time
import pickle as pk
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
method = orb #使用orb进行检测
#--------------------------------------------
dir="./static/Image"                 #保存图片的文件夹
desPath="./static/img_des.pkl"         #保存图片orb 特征的文件
#--------------------------------------------

desdic={}
now=0
for i in os.listdir(dir):
    print "processing"+str(now)
    now+=1

    path=os.path.join(dir,i) #获取图片路径
    try:
        if (os.path.isfile(path) and path.endswith(".jpg")): #确定是jpg文件
            img=cv2.imread(path,0)

            kp,des=method.detectAndCompute(img,None) #获取特征点和特征子
            if len(kp)==0:#没有检测到特征点
                continue
            else:
                desdic[path]=des #以路径作为键，特征子作为值
    except Exception,e:
        print Exception
        continue

file=open(desPath,"wb") #将信息保存到本地
pk.dump(desdic,file)
file.close()





