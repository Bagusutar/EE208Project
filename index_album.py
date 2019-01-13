#coding=utf8
import os,pprint
import cv2,time
import pickle as pk
target="./static/Image/album.txt"
import numpy as np
Data={}

f=open(target,"r") #打开专辑的文本
for line in f.readlines():
    k=line.split('\t')
    tmp=[int(k[0]),str(k[1]),str(k[2]),str(k[3]),str([k[4]]),str(k[5])[:-2]]  #专辑的相关信息
    print tmp
    Data[int(k[0])]=tmp #专辑ID作为值


file=open("./static/album.pkl","wb") #保存到本地
pk.dump(Data,file)
file.close()

