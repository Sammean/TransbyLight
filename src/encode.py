import numpy as np
import math
from PIL import Image
import struct
import os
from ffmpy import FFmpeg
import sys
import cv2
import copy
import re
def ReadFile_hex(filepath):
    fx = open(filepath, 'rb')
    size = os.path.getsize(filepath)
    list1=[]
    for i in range(int(size)):
        data=fx.read(1)
        data=data.hex()
        b = '{:08b}'.format(int(data,16))
        list1.append(b)
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
    BasicCode(890,0,img)
    for col in range(0,80,10):
        PrintPixel_10(img,880+col,70,255)
    for raw in range(0,80,10):
        PrintPixel_10(img,880,raw,255)
    BasicCode(0,890,img)
    for col in range(0,80,10):
        PrintPixel_10(img,col,880,255)
    for raw in range(0,80,10):
        PrintPixel_10(img,70,880+raw,255)
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
def encode(b_list,vlen):
    nEnough=len(b_list)%1128
    loc=0
    x=(0,80,160,240,320,400,480,560,640,720,800,880)
    y=(0,80,160,240,320,400,480,560,640,720,800,880)
    if nEnough!=0:
        Picnums=int(len(b_list)/1128)+1
        for i in range(0,1128-nEnough):
            b_list.append('00000000')
    else:
        Picnums=int(len(b_list)/1128)
    if(Picnums>vlen/1000*5):
        Picnums=int(vlen/1000*5)-1
    for i in range(0,Picnums):
        src=Image.new('RGB',(960,960),(255,255,255))
        AddLocCode(src)
        img=Image.new('RGB',(980,980),(255,255,255))
        img.paste(src,(10,10,970,970))
        img1=Image.new('RGB',(980,980),(255,255,255))
        for j in range(0,3):
            img1.save(str(j)+".png")
        for j in range(0,2):
            img1.save(str(Picnums+3+j)+".png")
        for cubes1 in range(1,11):
            list_8ch=[]
            for char in range(8):
                list_8ch.append(b_list[loc])
                loc+=1
            encode_cube(src,x[cubes1],y[0],list_8ch)
        for cubes_y in range(1,11):
            for cubes_x in range(12):
                list_8ch=[]
                for char in range(8):
                    list_8ch.append(b_list[loc])
                    loc+=1
                encode_cube(src,x[cubes_x],y[cubes_y],list_8ch)
        for cubes2 in range(1,12):
            list_8ch=[]
            for char in range(8):
                list_8ch.append(b_list[loc])
                loc+=1
            encode_cube(src,x[cubes2],y[11],list_8ch)
        tmp=Image.new('RGB',(980,980),(255,255,255))
        img.paste(src,(10,10,970,970))
        img.save(str(i+3)+".png")
    return Picnums+5
def FFmpegTrans(ofname):
    ff=FFmpeg(
        inputs={'%d.png':'-f image2 -r 5'},
        outputs={ofname:'-vcodec mpeg4'}
    )
    ff.run()
def DeleteImgs(Picnums):
    for i in range(Picnums):
        os.remove(str(i)+".png")
def main(argv):
    binfile=sys.argv[1]
    outfile=sys.argv[2]
    videolen=int(sys.argv[3],10)
    b_list=ReadFile_hex(binfile)
    Picnums=encode(b_list,videolen)
    FFmpegTrans(outfile)
    DeleteImgs(Picnums)
main(sys.argv)

