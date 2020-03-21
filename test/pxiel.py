import random
import numpy as np
import math
from PIL import Image
import struct
import os
from ffmpy import FFmpeg
import sys
import cv2
import copy
def ReadFile_asc(filepath):
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
def ReadFile_hex(filepath):
    fx = open(filepath, 'rb')
    size = os.path.getsize(filepath)
    list1=[]
    for i in range(int(size/4)):
        data=fx.read(4)
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
def encode(b_list):
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

    for i in range(0,Picnums):
        src=Image.new('RGB',(960,960),(255,255,255))
        AddLocCode(src)
        img=Image.new('RGB',(980,980),(255,255,255))
        img.paste(src,(10,10,970,970))
        img1=Image.new('RGB',(980,980),(255,255,255))
        for j in range(0,3):
            img1.save("D:/test1/t/"+str(j)+".png")
        for j in range(0,2):
            img1.save("D:/test1/t/"+str(Picnums+3+j)+".png")
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
        img.save("D:/test1/t/"+str(i+3)+".png")
def FFmpegTrans(ofname):

    ff=FFmpeg(
        inputs={'D:/test1/PicTrans/%d.png':'-f image2 -r 5'},
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
            cv2.imwrite("D:/test1/TransPics/"+sort+".png",frame)
            i=ord(sort)
            i+=1
            sort=chr(i)
        curFrame+=1
        rval,frame=video.read()

    video.release()
def decode(Picpath):
    Piclist = os.listdir(Picpath)
    RecoveryStr=""
    t_list=[]
    
    x=(8,88,168,248,328,408,488,568,648,728,808,888)
    y=(3,83,163,243,323,403,483,563,643,723,803,883)
    # x=(8,88,168,248,328,408,488,568,648,728,808,888)
    # y=(8,88,168,248,328,408,488,568,648,728,808,888)

    # x=(8,88,168,248,328,408,488,568,648,728,808,888)
    # y=(13,93,173,253,333,413,493,573,653,733,813,893)

    # x=(83,163,3,83,163,243,3,83,163,243,83,163,243)
    # y=(7,7,87,87,87,87,167,167,167,167,247,247,247)
    for pic in Piclist:
        if pic.endswith(".png"): 
            datastr="" 
            src = cv2.imread(Picpath+pic)
            #src=src[10:970,10:970]
            # cv2.imshow('x',src)
            # cv2.waitKey(0)
            img=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            img=cv2.blur(img,(3,3))
            #img=cv2.equalizeHist(img)
            thd=cv2.threshold(img,160,255,cv2.THRESH_BINARY)
            # cv2.imshow('xx',thd[1])
            # cv2.waitKey(0)
            for cubes1 in range(1,11):
                datastr+=decode_cube(thd,x[cubes1],y[0])
            for cubes_y in range(1,11):
                for cubes_x in range(12):
                    datastr+=decode_cube(thd,x[cubes_x],y[cubes_y])
            for cubes2 in range(1,12):
                datastr+=decode_cube(thd,x[cubes2],y[11])
            # for i in range(13):
            #     datastr+=decode_cube(thd,x[i],y[i])
            nums=int(len(datastr)/8)
            begain=0
            lenth=8
            for i in range(0,nums):
                ch=datastr[begain:lenth]
                #if(ch=='00000000'):break
                t_list.append(ch)
                begain=lenth
                lenth+=8
                RecoveryStr+=chr(int(ch,2))
                #RecoveryStr+=hex(int(ch,2))[2:]
    #print(RecoveryStr)
    encode(t_list)
    outfile=open("D:/test1/output.bin","w",encoding='utf-8')
    outfile.write(RecoveryStr)
    return t_list
def decode_cube(img,x,y):
    data=""
    for raw in range(y,y+80,10):
        if(raw>=960):raw=959
        for col in range(x,x+80,10):
            if(col>=960):col=959
            if(img[1][raw,col]==255):
                data+='0'
            else:
                data+='1'
    return data
def locim():
    files=os.listdir('D:/test1/TransPics/')
    for file in files:
        image=cv2.imread(os.path.join('D:/test1/TransPics/',file))
        #image=reshape_image(image)
        image,contours,hierachy=detecte(image)
        if(len(contours)==0):
            continue
        find(image,file,contours,np.squeeze(hierachy))
def reshape_image(image):
    '''归一化图片尺寸：短边400，长边不超过800，短边400，长边超过800以长边800为主'''
    width,height=image.shape[1],image.shape[0]
    min_len=width
    scale=width*1.0/400
    new_width=400
    new_height=int(height/scale)
    if new_height>800:
        new_height=800
        scale=height*1.0/800
        new_width=int(width/scale)
    out=cv2.resize(image,(new_width,new_height))
    return out
def detecte(image):
    '''提取所有轮廓'''
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,gray=cv2.threshold(gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
    contours,hierachy=cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return image,contours,hierachy
def compute_1(contours,i,j):
    '''最外面的轮廓和子轮廓的比例'''
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2==0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 49.0 / 25):
        return True
    return False
def compute_2(contours,i,j):
    '''子轮廓和子子轮廓的比例'''
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2==0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 25.0 / 9):
        return True
    return False
def compute_center(contours,i):
    '''计算轮廓中心点'''
    M=cv2.moments(contours[i])
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return cx,cy
def detect_contours(vec):
    '''判断这个轮廓和它的子轮廓以及子子轮廓的中心的间距是否足够小'''
    distance_1=np.sqrt((vec[0]-vec[2])**2+(vec[1]-vec[3])**2)
    distance_2=np.sqrt((vec[0]-vec[4])**2+(vec[1]-vec[5])**2)
    distance_3=np.sqrt((vec[2]-vec[4])**2+(vec[3]-vec[5])**2)
    if sum((distance_1,distance_2,distance_3))/3<3:
        return True
    return False
def juge_angle(rec):
    '''判断寻找是否有三个点可以围成等腰直角三角形'''
    if len(rec)<3:
        return -1,-1,-1
    for i in range(len(rec)):
        for j in range(i+1,len(rec)):
            for k in range(j+1,len(rec)):
                distance_1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
                distance_2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
                distance_3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
                if abs(distance_1-distance_2)<5:
                    if abs(np.sqrt(np.square(distance_1)+np.square(distance_2))-distance_3)<5:
                        return i,j,k
                elif abs(distance_1-distance_3)<5:
                    if abs(np.sqrt(np.square(distance_1)+np.square(distance_3))-distance_2)<5:
                        return i,j,k
                elif abs(distance_2-distance_3)<5:
                    if abs(np.sqrt(np.square(distance_2)+np.square(distance_3))-distance_1)<5:
                        return i,j,k
    return -1,-1,-1
def find(image,image_name,contours,hierachy,root=0):
    '''找到符合要求的轮廓'''
    rec=[]
    for i in range(len(hierachy)):
        child = hierachy[i][2]
        child_child=hierachy[child][2]
        if child!=-1 and hierachy[child][2]!=-1:
            if compute_1(contours, i, child) and compute_2(contours,child,child_child):
                cx1,cy1=compute_center(contours,i)
                cx2,cy2=compute_center(contours,child)
                cx3,cy3=compute_center(contours,child_child)
                if detect_contours([cx1,cy1,cx2,cy2,cx3,cy3]):
                    rec.append([cx1,cy1,cx2,cy2,cx3,cy3,i,child,child_child])
    '''计算得到所有在比例上符合要求的轮廓中心点'''
    i,j,k=juge_angle(rec)
    if i==-1 or j== -1 or k==-1:
        return
    ts = np.concatenate((contours[rec[i][6]], contours[rec[j][6]], contours[rec[k][6]]))
    rect = cv2.minAreaRect(ts)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    result=copy.deepcopy(image)
    # cv2.imshow('s',result)     
    #cv2.drawContours(result, [box], 0, (0, 0, 255), 2)
    #result=crop(result,box)
    #result=rotate_bound(result,90+rect[2])
    # cv2.imshow('r',result)     
    result=crop(result,box)
    # cv2.imshow('rr',result)
    # cv2.waitKey(0)
    result=cv2.resize(result,(960,960))
    cv2.imwrite("D:/test1/Processed/"+image_name,result)
    return
def crop(result,box):

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    Xs.sort()
    Ys.sort()
    x1 = Xs[1]
    x2 = Xs[3]
    y1 = Ys[1]
    y2 = Ys[3]
    hight = y2 - y1
    width = x2 - x1
    cropImg = result[y1:y1+hight, x1:x1+width]
    # cv2.imshow('cp',cropImg)
    # cv2.waitKey(0)
    return cropImg
def rotate_bound(image, angle):    

    (h, w) = image.shape[:2]    
    (cX, cY) = (w // 2, h // 2)      
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)    
    cos = np.abs(M[0, 0])    
    sin = np.abs(M[0, 1])        
    nW = int((h * sin) + (w * cos))    
    nH = int((h * cos) + (w * sin))       
    M[0, 2] += (nW / 2) - cX    
    M[1, 2] += (nH / 2) - cY       
    return cv2.warpAffine(image, M, (nW, nH))
def valid(b_list,r_list,ofname):
    vfile=open(ofname,"wb")
    f_list=[]
    for i in range(min(len(b_list),len(r_list))):
        ch=''
        for j in range(8):
            if(b_list[i][j]==r_list[i][j]):
                ch+='1'
            else:
                ch+='0'
        ch=bin(ch)
        vfile.write(hex(int(ch,2)))
def wuma():
    for i in range(3,9):
        src1 = cv2.imread("D:/test/PicTrans/"+str(i)+".png")
        src2 = cv2.imread("D:/test/t/"+str(i)+".png")
        # src1=src1[5:165,5:165]
        # thd=cv2.threshold(src2,165,255,cv2.THRESH_BINARY)[1]
        src = cv2.bitwise_xor(src2, src1)
        cv2.imwrite("D:/test/xor/"+str(i)+".png",src)
        # cv2.imshow("src",src1)
        # cv2.imshow("xor", src)
        # cv2.waitKey(0)    


if __name__ == '__main__':
    #b_list=ReadFile_hex("D:/test1/1.bin")
    #b_list=ReadFile("D:/test1/1.bin")        
    #encode(b_list)
    #FFmpegTrans("D:/test1/output/t.mp4")
    # VideotoPics("D:/test1/tt.mp4")
    # locim()
    r_list=decode("D:/test1/Processed/")
    #valid(b_list,r_list,"D:/test1/valid.bin")