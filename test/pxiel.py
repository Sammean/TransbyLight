import numpy as np
import math
from PIL import Image
import struct
import os
from ffmpy import FFmpeg
import sys
import cv2
def ReadFile(filepath):
    binfile = open(filepath, 'rb')
    size = os.path.getsize(filepath)
    list1=[]
    for i in range(size):
        data = binfile.read(1)
        num=struct.unpack('B',data)
        b = '{:08b}'.format(num[0])
        # OrE=b.count('1')#偶校验
        # if(OrE%2)==0:#偶数个1
        #     bb='0'+b[1:8]
        # else:
        #     bb='1'+b[1:8]
        list1.append(b)
    binfile.close()
    return list1
def AddLocCode(img):
    def BasicCode(x,y,img):
        for col in range(0,70,10):
            PrintPixel_10(img,x+col,y,0)
        for col in range(0,70,10):
            PrintPixel_10(img,x+col,y+60,0)
        for col in range(0,60,10):
            PrintPixel_10(img,x+10+col,y+10,255)
        for col in range(0,60,10):
            PrintPixel_10(img,x+10+col,y+50,255)
        for raw in range(0,50,10):
            PrintPixel_10(img,x,y+10+raw,0)
        for raw in range(0,50,10):
            PrintPixel_10(img,x+60,y+10+raw,0)
        for raw in range(0,30,10):
            PrintPixel_10(img,x+10,y+20+raw,255)
        for raw in range(0,30,10):
            PrintPixel_10(img,x+50,y+20+raw,255)
        for raw in range(0,30,10):
            for col in range(0,30,10):
                PrintPixel_10(img,x+20+col,y+20+raw,0)
    BasicCode(0,0,img)
    for col in range(0,80,10):
        PrintPixel_10(img,col,70,255)
    for raw in range(0,80,10):
        PrintPixel_10(img,70,raw,255)
    BasicCode(250,0,img)
    for col in range(0,80,10):
        PrintPixel_10(img,240+col,70,255)
    for raw in range(0,80,10):
        PrintPixel_10(img,240,raw,255)
    BasicCode(0,250,img)
    for col in range(0,80,10):
        PrintPixel_10(img,col,240,255)
    for raw in range(0,80,10):
        PrintPixel_10(img,70,240+raw,255)
def PrintPixel_10(img,x,y,color):
    for r in range(10):
        for c in range(10):
            img.putpixel([x+c,y+r],(color,color,color))
def encode_cube(img,x,y,list):
    for i in range (8):
            for j in range (8):
                if(list[i][j]=='0'):
                    PrintPixel_10(img,x,y,255)
                else:
                    PrintPixel_10(img,x,y,0)
                x+=10
            x-=80
            y+=10
def encode(b_list):
    nEnough=len(b_list)%104
    loc=0
    x=(80,160,0,80,160,240,0,80,160,240,80,160,240)
    y=(0,0,80,80,80,80,160,160,160,160,240,240,240)
    if nEnough!=0:
        Picnums=int(len(b_list)/104)+1
        for i in range(0,104-nEnough):
            b_list.append('00000000')
    else:
        Picnums=int(len(b_list)/104)

    for i in range(0,Picnums):
        src=Image.new('RGB',(320,320),(255,255,255))
        AddLocCode(src)
        img=Image.new('RGB',(340,340),(255,255,255))
        img.paste(src,(10,10,330,330))
        img1=Image.new('RGB',(340,340),(255,255,255))
        for j in range(0,5):
            img1.save("D:/test/PicTrans/"+str(j)+".png")
        for j in range(0,2):
            img1.save("D:/test/PicTrans/"+str(Picnums+5+j)+".png")
        for cubes in range(13):
            list_8ch=[]
            for char in range(8):
                list_8ch.append(b_list[loc])
                loc+=1
            encode_cube(src,x[cubes],y[cubes],list_8ch)
        tmp=Image.new('RGB',(340,340),(255,255,255))
        img.paste(src,(10,10,330,330))
        img.save("D:/test/PicTrans/"+str(i+5)+".png")
def FFmpegTrans(ofname):

    ff=FFmpeg(
        inputs={'D:/test/PicTrans/%d.png':'-f image2 -r 5'},
        outputs={ofname:'-vcodec mpeg4'}
    )
    ff.run()
def VideotoPics(VideoPath):
    video=cv2.VideoCapture(VideoPath)
    sort='a'
    curFrame=0
    if video.isOpened():
        rval,frame=video.read()
    else:
        rval=False
    while rval:
        if curFrame%6==0:
            cv2.imwrite("D:/test/TransPics/"+sort+".png",frame)
            i=ord(sort)
            i+=1
            sort=chr(i)
        curFrame+=1
        rval,frame=video.read()

    video.release()
def decode(Picpath):
    Piclist = os.listdir(Picpath)
    RecoveryStr=""
    x=(85,165,5,85,165,245,5,85,165,245,85,165,245)
    y=(0,0,80,80,80,80,160,160,160,160,240,240,240)
    for pic in Piclist:
        if pic.endswith(".png"): 
            datastr="" 
            src = cv2.imread(Picpath+pic)
            #src=src[5:165,5:165]
            img=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            img=cv2.blur(img,(3,3))
            #img=cv2.equalizeHist(img)
            thd=cv2.threshold(img,160,255,cv2.THRESH_BINARY)
            cv2.imshow('xx',thd[1])
            cv2.waitKey(0)
            for i in range(13):
                datastr+=decode_cube(thd,x[i],y[i])
            nums=int(len(datastr)/8)
            begain=0
            lenth=8
            
            #t_list=[]
            for i in range(0,nums):
                ch=datastr[begain:lenth]
                #t_list.append(ch)
                begain=lenth
                lenth+=8
                RecoveryStr+=chr(int(ch,2))
    print(RecoveryStr)
            #encode(t_list)
def decode_cube(img,x,y):
    data=""
    for raw in range(y,y+80,10):
        for col in range(x,x+80,10):
            if(img[1][raw,col]==255):
                data+='0'
            else:
                data+='1'
    return data

# b_list=ReadFile("D:/test/test.bin")        
# encode(b_list)
# FFmpegTrans("D:/test/output/t.mp4")
#VideotoPics("D:/test/t.mp4")
#decode("D:/test/Processed/")