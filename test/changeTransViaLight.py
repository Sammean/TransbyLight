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
    list2=[]
    #j=0
    for i in range(size):
        data = binfile.read(1)
        num=struct.unpack('B',data)
        b = '{:08b}'.format(num[0])
        list2.append(b)
    #     if j<648:
    #         b = '{:08b}'.format(num[0])
    #         list1.append(b)
    #         j+=1
    #     else:
    #         list1.append('#')
    #         list1.append('{:08b}'.format(num[0]))
    #         j=0

    # list1.append('#')
    i=0
    length=len(list2)
    for i in range(length):#汉明码偶配原则
       list3=[]
       trans=list[i]
       for j in range(8):#一次读8位，形成16位汉明码，后两位补0
          a=int(trans[j])#字符型转成int型，方便相加进行判断
          list3.append(a)
       if((list3[0]+list3[1]+list3[3]+list3[4]+list3[6])%2!=0)#1相加起来为奇数，补1---第一位
           list1.append(1)
       else
           list1.append(0)
       if((list3[0]+list3[2]+list3[3]+list3[5]+list3[6])%2!=0)#1相加起来为奇数，补1------第二位
           list1.append(1)
       else
           list1.append(0)
       list1.append(list3[0])#添加第三位，为原数据的第一位
       if((list3[1]+list3[2]+list3[3]+list3[7])%2!=0)#1相加起来为奇数，补1-----第四位
           list1.append(1)
       else
           list1.append(0)
       for j in range(3):
           list1.append(list3[++j])#原数据234输入5，6，7
       if((list3[4]+list3[5]+list3[6]+list3[7])%2!=0)#1相加起来为奇数，补1-----第八位
           list1.append(1)
       else
           list1.append(0)
       for j in range(4):#原数据5678输入9，10，11，12
           list1.append(list3[j+4])
       for j in range(4):#补0补满16位
           list1.append(0)
    binfile.close()
    return list1
def AddLocCode(img):
    def BasicCode(x,y,img):
        for col in range(7):
            img.putpixel([x+col,y],(0,0,0))
        for col in range(7):
            img.putpixel([x+col,y+6],(0,0,0))
        for col in range(5):
            img.putpixel([x+1+col,y+1],(255,255,255))
        for col in range(5):
            img.putpixel([x+1+col,y+5],(255,255,255))
        for raw in range(5):
            img.putpixel([x,y+1+raw],(0,0,0))
        for raw in range(5):
            img.putpixel([x+6,y+1+raw],(0,0,0))
        for raw in range(3):
            img.putpixel([x+1,y+2+raw],(255,255,255))
        for raw in range(3):
            img.putpixel([x+5,y+2+raw],(255,255,255))
        for raw in range(3):
            for col in range(3):
                img.putpixel([x+2+col,y+2+raw],(0,0,0))
    BasicCode(0,0,img)
    for col in range(8):
        img.putpixel([col,7],(255,255,255))
    for raw in range(8):
        img.putpixel([7,raw],(255,255,255))
    BasicCode(img.size[0]-7,0,img)
    for col in range(8):
        img.putpixel([img.size[0]-8+col,7],(255,255,255))
    for raw in range(8):
        img.putpixel([img.size[0]-8,raw],(255,255,255))
    BasicCode(0,img.size[0]-7,img)
    for col in range(8):
        img.putpixel([col,img.size[0]-8],(255,255,255))
    for raw in range(8):
        img.putpixel([7,img.size[0]-8+raw],(255,255,255))
def encode(b_list):


    i=0
    j=0
    #begain=0
    Picnums=int(len(b_list)/648)
    # for num in range(Picnums):
    #     b_list.remove('#')
    frame=Image.new('RGB',(80,80),(0,0,0))
    frame.save('0.png')
    frame.save('1.png')
    frame.save(str(Picnums+2)+'.png')
    for num in range(0,Picnums):
        # Locate=b_list.index('#')
        MAX = 80
        # begain=Locate
        img = Image.new("RGB",(MAX,MAX))
        AddLocCode(img)
        for y in range (8,MAX):
            for x in range (8,MAX):
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
                
                
                
            list=[]#存储纠正后的数据
            i=0
            while i<size:         #size为列表长度，列表    最好传入int型，如果是字符型就用中间那个转换字符成int型
                translist=[]#储存十六位读数
                for j in range(16):
                   #a=int(list2[i])#字符型转成int型，方便相加进行判断
                   translist.append(list2[i])#list2指解码后产生的数组
                   i+=1
                p1=(translist[0]+translist[2]+translist[4]+translist[6]+translist[8]+translist[10])%2#余数形成p1(1,3,5,7,9,11)
                p2=(translist[1]+translist[2]+translist[5]+translist[6]+translist[9]+translist[10])%2#余数形成p2(2,3,6,7,10,11)
                p3=(translist[3]+translist[4]+translist[5]+translist[6]+translist[11])%2#余数形成p3(4,5,6,7,12)
                p4=(translist[7]+translist[8]+translist[9]+translist[10]+translist[11])%2#余数形成p4(8,9,10,11,12)
                p=p1+p2*2+p3*4+p4*8
                if(p<13 and p!=1 and p!=2 and p!=4 and p!=8)#排除1，2，4，8号纠错码，并规定了数据的范围
                   translist[p]=(translist[p]+1)%2#原数据为1：（1+1）%2=0；为0：（1+0）%2=1
                list.append(translist[3])
                for j in range(3):#5,6,7->
                   list.append(translist[j+4])
                for j in range(4):#9,10,11,12->
                   list.append(translist[j+8])
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

# b_list=ReadFile("D:/test/ts.bin")
# encode(b_list)
# FFmpegTrans("D:/test/output/t.mp4")
#VideotoPics("D:/test/tt.mp4")
decode("D:/test/TransPics/")

