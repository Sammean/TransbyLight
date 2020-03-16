import cv2
from PIL import Image
import os
import struct
import math
from ffmpy import FFmpeg
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
def ReadFile(filepath):
    binfile = open(filepath, 'rb') #打开二进制文件
    size = os.path.getsize(filepath) #获得文件大小
    list1=[]
    for i in range(size):
        data = binfile.read(1) #每次输出一个字节
        num=struct.unpack('B',data)#转化成十进制
        b = '{:08b}'.format(num[0])
        list1.append(b)
    binfile.close()
    return list1
def encode(b_list):
    list1=[]
    for i in range(len(b_list)):
        data = b_list[i]
        num=struct.unpack('B',data)
        b = '{:08b}'.format(num[0])
        list1.append(b)
    i=0
    j=0
    Picnums=1
    MAX =int(math.sqrt(len(b_list)/50))+8
    for num in range(0,Picnums):
        img = Image.new("RGB",(MAX,MAX))
        AddLocCode(img)
        for y in range (8,MAX):
            for x in range (8,MAX):
                if(list1[i][j]=='0'):
                    img.putpixel([x,y],(255, 255, 255))
                else:
                    img.putpixel([x,y],(0,0, 0))
                      
                if j==7:
                    i=i+1
                    j=0
                else:
                    j=j+1

        ofname="D:/test/"+str(num+1)+".png"
        #img.show()
        img.save(ofname)
def FFmpegTrans(ofname):

    ff=FFmpeg(
        inputs={'D:/test/TransPics/%d.png':'-f image2 -r 0.5'},
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
        cv2.imwrite("D:/test/PicTrans/"+str(i)+".png",frame)
        i=i+1
        rval,frame=video.read()

    video.release()
def decode(Picpath):
    ofile=open("D:/test/1.txt",'w',encoding='utf-8')
    path = Picpath
    Piclist = os.listdir(path)
    Picnums=len(Piclist)
    i=0
    datastr=""
    for pic in range(0,Picnums):
        if Piclist[pic].endswith(".png"):
            picture = path +Piclist[pic]
            src = cv2.imread(picture)
            gray=cv2.cvtColor(src,cv2.COLOR_RGB2GRAY)
            img=cv2.threshold(gray,127,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
            size1=img.shape[0]
            size2=img.shape[1]
            for y in range(8,size1):
                for x in range(8,size2):
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
    ofile.write(RecoveryStr)
    ofile.close()
def wuma():
    for i in range(102,110):
        src1 = cv2.imread("D:/test/PicTrans/"+chr(i)+".png")
        src2 = cv2.imread("D:/test/t/"+chr(i+1)+".png")
        # src1=src1[5:165,5:165]
        # thd=cv2.threshold(src2,165,255,cv2.THRESH_BINARY)[1]
        src = cv2.bitwise_xor(src2, src1)
        cv2.imshow("xor", src)
        cv2.waitKey(0)

# b_list=ReadFile("D:/test/in.bin")
# encode(b_list)

# FFmpegTrans("D:/test/t.mp4")
# VideotoPics("D:/test/t.mp4")
#decode("D:/test/")
wuma()