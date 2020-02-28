# TransbyLight

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
        Firnum=num[0]
        if(Firnum==10):
            list1.append('#')
            continue
        if(Firnum==13):
            continue
        else:
            b = '{:08b}'.format(num[0])
            list1.append(b)    
    binfile.close()
    return list1

def encode(b_list):

    i=0
    j=0
    begain=0
    Picnums=b_list.count('#')
    for num in range(0,Picnums):
        PicLables=str(Picnums-1)
        Locate=b_list.index('#')
        b_list.remove('#')
        MAX = int(math.sqrt((Locate-begain)*8))
        begain=Locate
        img = Image.new("RGB",(MAX,MAX))
        for y in range (0,MAX):
            for x in range (0,MAX):
                if(b_list[i][j]=='0'):
                    img.putpixel([x,y],(255, 255, 255))
                else:
                    img.putpixel([x,y],(0,0, 0))
                      
                if j==7:
                    i=i+1
                    j=0
                else:
                    j=j+1

        ofname="D:/test/output/"+PicLables+".png"
        #img.show()
        img.save(ofname)
        Picnums=Picnums-1
def FFmpegTrans(ofname):

    ff=FFmpeg(
        inputs={'%d.png':'-f image2 -r 1'},
        outputs={ofname:'-vcodec mpeg4'}
    )
    print(ff.cmd)
    ff.run()
def decode(Picpath,ofname):
    path = Picpath
    Piclist = os.listdir(path)
    i=0
    datastr=""
    for pic in Piclist:
        if pic.endswith('.png'): 
            pic = path + pic
            img = cv2.imread(pic)
            size=img.shape[0]
            for y in range(0,size):
                for x in range(0,size):
                    (b,g,r)=img[x,y]
                    if((b,g,r)==(255,255,255)):
                        datastr+='1'
                    else:
                        datastr+='0'
                    i+=1
            nums=int(len(datastr)/8)
            begain=0
            lenth=8
            for i in range(0,nums):
                ch=datastr[begain:lenth]
                begain=lenth
                lenth+=8
                print(int(ch,2))            

def main():
    ifname=sys.argv[1]
    ofname=sys.argv[2]
    timing=sys.argv[3]
  .  b_list=ReadFile(ifname)
    encode(b_list)
    FFmpegTrans(ofname)

if __name__ == "__main__":
    main()
b_list=ReadFile("D:/test/output/ts.bin")
encode(b_list)
decode(Picpath)
