#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,pickle as pk
import cv2
reload(sys)


def Com(x, y): #比较函数，匹配点的数目为第一关键字，降序排列；距离之和为第二关键字，升序排列

    if x[0] > y[0]:
        return -1
    if x[0] == y[0] and x[1] < y[1]:
        return -1
    return 1




orb = cv2.ORB_create(nfeatures=300)
def Search_img(target,img_data,album_data):

    target_gray = cv2.imread(target, cv2.IMREAD_GRAYSCALE)#打开目标图像

    method = orb
    kp, des = method.detectAndCompute(target_gray, None) #获取关键点和特征子
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True) #设置BFMatcher参数

    Result = []

    for k, v in img_data.items(): #遍历本地储存的特征子
        matches = bf.match(des, v) #进行匹配
        Sum = 0
        Total = 0
        for i in range(len(matches)):
            if matches[i].distance < 50: #汉明距离小于50即认为匹配
                Sum += 1 #匹配数量加一
                Total += matches[i].distance #更新距离总和

        if Sum != 0:
            Result.append([Sum, Total, k])

    Result.sort(Com)#排序
    pipei =[]
    for i in range(0,min(len(Result),100)): #对于前一百个结果


        ID=int((Result[i][2]).replace('\\', '/') [15:-4] ) #获取专辑ID
        tmp=[(Result[i][2]).replace('\\', '/') ]
        tmp.extend(album_data[ID]) #获取专辑信息
        pipei.append(tmp)

    return target,pipei,len(pipei) #返回结果信息
