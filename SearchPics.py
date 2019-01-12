#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,pickle as pk
import cv2
reload(sys)


def Com(x, y):

    if x[0] > y[0]:
        return -1
    if x[0] == y[0] and x[1] < y[1]:
        return -1
    return 1




orb = cv2.ORB_create(nfeatures=300)
def Search_img(target,img_data,album_data):

    target_gray = cv2.imread(target, cv2.IMREAD_GRAYSCALE)

    method = orb
    kp, des = method.detectAndCompute(target_gray, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    pipei = " "

    Result = []

    for k, v in img_data.items():
        matches = bf.match(des, v)
        Sum = 0
        Total = 0
        # matches = sorted(matches, key = lambda x:x.distance)
        for i in range(len(matches)):
            if matches[i].distance < 50:
                Sum += 1
                Total += matches[i].distance

        if Sum != 0:
            Result.append([Sum, Total, k])


    Result.sort(Com)

    pipei =[]
    print
    print len(Result)
    print

    for i in range(0,min(len(Result),100)):


        ID=int((Result[i][2]).replace('\\', '/') [15:-4] )
        tmp=[(Result[i][2]).replace('\\', '/') ]
        tmp.extend(album_data[ID])
        pipei.append(tmp)



    return target,pipei,len(pipei)
