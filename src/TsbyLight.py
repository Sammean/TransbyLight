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
        for col in range(0,35,5):
            PrintPixel_5(img,x+col,y,0)
        for col in range(0,35,5):
            PrintPixel_5(img,x+col,y+30,0)
        for col in range(0,30,5):
            PrintPixel_5(img,x+5+col,y+5,255)
        for col in range(0,30,5):
            PrintPixel_5(img,x+5+col,y+25,255)
        for raw in range(0,25,5):
            PrintPixel_5(img,x,y+5+raw,0)
        for raw in range(0,25,5):
            PrintPixel_5(img,x+30,y+5+raw,0)
        for raw in range(0,15,5):
            PrintPixel_5(img,x+5,y+10+raw,255)
        for raw in range(0,15,5):
            PrintPixel_5(img,x+25,y+10+raw,255)
        for raw in range(0,15,5):
            for col in range(0,15,5):
                PrintPixel_5(img,x+10+col,y+10+raw,0)
    BasicCode(0,0,img)
    for col in range(0,40,5):
        PrintPixel_5(img,col,35,255)
    for raw in range(0,40,5):
        PrintPixel_5(img,35,raw,255)
    BasicCode(125,0,img)
    for col in range(0,40,5):
        PrintPixel_5(img,120+col,35,255)
    for raw in range(0,40,5):
        PrintPixel_5(img,120,raw,255)
    BasicCode(0,125,img)
    for col in range(0,40,5):
        PrintPixel_5(img,col,120,255)
    for raw in range(0,40,5):
        PrintPixel_5(img,35,120+raw,255)
def PrintPixel_5(img,x,y,color):
    for r in range(5):
        for c in range(5):
            img.putpixel([x+c,y+r],(color,color,color))
def encode_cube(img,x,y,list):
    for i in range (8):
            for j in range (8):
                if(list[i][j]=='0'):
                    PrintPixel_5(img,x,y,255)
                else:
                    PrintPixel_5(img,x,y,0)
                x+=5
            x-=40
            y+=5
def encode(b_list):
    nEnough=len(b_list)%104
    loc=0
    x=(40,80,0,40,80,120,0,40,80,120,40,80,120)
    y=(0,0,40,40,40,40,80,80,80,80,120,120,120)
    if nEnough!=0:
        Picnums=int(len(b_list)/104)+1
        for i in range(0,104-nEnough):
            b_list.append('00000000')
    else:
        Picnums=int(len(b_list)/104)

    for i in range(Picnums):
        src=Image.new('RGB',(160,160),(0,0,0))
        AddLocCode(src)
        img=Image.new('RGB',(170,170),(255,255,255))
        img.paste(src,(5,5,165,165))
        for j in range(5):
            img.save("D:/test/t/"+str(j)+".png")
        img1=Image.new('RGB',(170,170),(0,0,0))
        for j in range(2):
            img1.save("D:/test/t/"+str(Picnums+5+j)+".png")
        for cubes in range(13):
            list_8ch=[]
            for char in range(8):
                list_8ch.append(b_list[loc])
                loc+=1
            encode_cube(src,x[cubes],y[cubes],list_8ch)
        tmp=Image.new('RGB',(170,170),(255,255,255))
        img.paste(src,(5,5,165,165))
        img.save("D:/test/t/"+str(i+5)+".png")
def FFmpegTrans(ofname):

    ff=FFmpeg(
        inputs={'D:/test/PicTrans/%d.png':'-f image2 -r 5'},
        outputs={ofname:'-vcodec mpeg4'}
    )
    ff.run()
def VideotoPics(VideoPath):
    video=cv2.VideoCapture(VideoPath)
    i=0
    curFrame=0
    if video.isOpened():
        rval,frame=video.read()
    else:
        rval=False
    while rval:
        if curFrame%6==0:
            cv2.imwrite("D:/test/tt/"+str(i)+".png",frame)
            i=i+1
        curFrame+=1
        rval,frame=video.read()

    video.release()
def decode(Picpath):
    Piclist = os.listdir(Picpath)
    datastr=""
    x=(42,82,2,42,82,122,2,42,82,122,42,82,122)
    y=(1,1,40,40,40,40,80,80,80,80,121,121,121)
    for pic in Piclist:
        if pic.endswith(".png"):  
            src = cv2.imread(Picpath+pic)
            img=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            thd=cv2.threshold(img,160,255,cv2.THRESH_BINARY)
            for i in range(13):
                datastr+=decode_cube(thd,x[i],y[i])
            nums=int(len(datastr)/8)
            begain=0
            lenth=8
            RecoveryStr=""
            t_list=[]
            for i in range(0,nums):
                ch=datastr[begain:lenth]
                t_list.append(ch)
                begain=lenth
                lenth+=8
                RecoveryStr+=chr(int(ch,2))
        print(RecoveryStr)
            #encode(t_list)
def decode_cube(img,x,y):
    data=""
    for raw in range(y,y+40,5):
        for col in range(x,x+40,5):
            if(img[1][raw,col]==255):
                data+='0'
            else:
                data+='1'
    return data

# b_list=ReadFile("D:/test/test.bin")        
# encode(b_list)
#FFmpegTrans("D:/test/output/t.mp4")
#VideotoPics("D:/test/t.mp4")
decode("D:/test/t1_10%/test/")
