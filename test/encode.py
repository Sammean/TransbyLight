import numpy as np
import math
from PIL import Image
import struct
import os
from ffmpy import FFmpeg
import sys
def ReadFile(filepath):
    binfile = open(filepath, 'rb') #打开二进制文件
    size = os.path.getsize(filepath) #获得文件大小
    flag=0#记录
    a=0#记录余数
    b=0#
    list1=[]#建立空列表，利用列表记录二进制数据
    list2=[]#建立空列表，逆序储存，方便转化
    for i in range(size):
        data = binfile.read(1) #每次输出一个字节
        num=struct.unpack('B',data)#转化成十进制
        Firnum=num[0]
        if(Firnum==10):
            list1.append(Firnum)
            continue
        for j in range(8):#转化成二进制
             list2.append(Firnum%2)
             Firnum=(int)(Firnum/2)
        for h in range(8):
             list1.append(list2[7-h])
    list2.clear()#清除list2的数据
    binfile.close()
    return list1

def encode(b_list):

    i=0
    begain=0
    Picnums=b_list.count(10)
    for num in range(0,Picnums):
        PicLables=str(Picnums-1)
        Locate=b_list.index(10)
        b_list.remove(10)
        MAX = int(math.sqrt(Locate-begain))
        begain=Locate
        img = Image.new("RGB",(MAX,MAX))
        for y in range (0,MAX):


            for x in range (0,MAX):


                if(b_list[i]==1):

                    img.putpixel([x,y],(255, 255, 255))


                else:

                    img.putpixel([x,y],(0,0, 0))

           
                i = i+1

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

def OpencvTrans():
    path = 'D:/test/output/'
    filelist = os.listdir(path)

    fps = 1
    size = (70, 70)#需要转为视频的图片的尺寸
    #可以使用cv2.resize()进行修改

    video = cv2.VideoWriter("D:/test/VideoTest1.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    #视频保存在当前目录下

    for item in filelist:
        if item.endswith('.png'): 
        #找到路径中所有后缀名为.png的文件，可以更换为.jpg或其它
            item = path + item
            img = cv2.imread(item)
            video.write(img)

    video.release()
    cv2.destroyAllWindows()

# def main():
#     ifname=sys.argv[1]
#     ofname=sys.argv[2]
#     timing=sys.argv[3]
#   .  b_list=ReadFile(ifname)
#     encode(b_list)
#     FFmpegTrans(ofname)

# if __name__ == "__main__":
#     main()
b_list=ReadFile("D:/test/ts.bin")
encode(b_list)