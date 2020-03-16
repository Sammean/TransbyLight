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
    #j=0
    for i in range(size):
        data = binfile.read(1)
        num=struct.unpack('B',data)
        b = '{:08b}'.format(num[0])
        list1.append(b)
    #     if j<648:
    #         b = '{:08b}'.format(num[0])
    #         list1.append(b)
    #         j+=1
    #     else:
    #         list1.append('#')
    #         list1.append('{:08b}'.format(num[0]))
    #         j=0

    # list1.append('#')
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

def encode(b_list):


    i=0
    j=0
    #begain=0
    #Picnums=int(len(b_list)/648)
    Picnums=1
    # for num in range(Picnums):
    #     b_list.remove('#')
    frame=Image.new('RGB',(160,160),(0,0,0))
    AddLocCode(frame)
    frame.save('0.png')
    frame.save('1.png')
    frame.save(str(Picnums+2)+'.png')
    for num in range(0,Picnums):
        img = Image.new("RGB",(160,160))
        AddLocCode(img)
        for y in range (8,142):
            for x in range (8,138):
                if(b_list[i][j]=='0'):
                    img.putpixel([x,y],(255, 255, 255))
                else:
                    img.putpixel([x,y],(0,0, 0))
                      
                if j==7:
                    i=i+1
                    j=0
                else:
                    j=j+1

        ofname=str(num+2)+".png"
        #img.show()
        img.save(ofname)
def FFmpegTrans(ofname):

    ff=FFmpeg(
        inputs={'%d.png':'-f image2 -r 1'},
        outputs={ofname:'-vcodec mpeg4'}
    )
    print(ff.cmd)
    ff.run()
def VideotoPics(VideoPath):
    video=cv2.VideoCapture(VideoPath)
    i=1
    if video.isOpened():
        rval,frame=video.read()
    else:
        rval=False
    while rval:
        cv2.imwrite("D:/test/TransPics/"+str(i)+".png",frame)
        i=i+1
        rval,frame=video.read()
    video.release()
def decode(Picpath):
    path = Picpath
    Piclist = os.listdir(path)
    Picnums=5
    i=0
    datastr=""
    for pic in range(59,89,119,149,179):
        if Piclist[pic].endswith(".png"):
            picture = path +Piclist[pic]
            src = cv2.imread(picture)
            gray=cv2.cvtColor(src,cv2.COLOR_RGB2GRAY)
            img=cv2.threshold(gray,127,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
            size=img.shape[0]
            for y in range(8,size):
                for x in range(8,size):
                    bit=img[y,x]
                    if(bit==0):
                        datastr+='1'
                    else:
                        datastr+='0'
                    i+=1
            nums=int(len(datastr)/8)
            begain=0
            lenth=8
            RecoveryStr=""
            for i in range(0,nums):
                ch=datastr[begain:lenth]
                begain=lenth
                lenth+=8
                RecoveryStr+=chr(int(ch,2))
    print(RecoveryStr)


# def main():
#     ifname=sys.argv[1]
#     ofname=sys.argv[2]
#     timing=sys.argv[3]
#     b_list=ReadFile(ifname)
#     encode(b_list)
#     FFmpegTrans(ofname)

# if __name__ == "__main__":
#     main()

b_list=ReadFile("D:/test/1.bin")
encode(b_list)
# FFmpegTrans("D:/test/output/t.mp4")
#VideotoPics("D:/test/tt.mp4")
#decode("D:/test/TransPics/")

