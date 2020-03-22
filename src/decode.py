import numpy as np
import math
from PIL import Image
import struct
import os
import sys
import cv2
import copy
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
            cv2.imwrite("D:/ct/"+str(i)+".png",frame)
            i+=1
        curFrame+=1
        rval,frame=video.read()

    video.release()
def locim():
    files=os.listdir("D:/ct/")
    for file in files:
        if file.endswith('.png'):
            image=cv2.imread(os.path.join('D:/ct/',file))
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
    cv2.imwrite(image_name,result)
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
        vfile.write(struct.pack('B',int(ch,2)))
def decode(outfile):
    Piclist = os.listdir(os.path.split(os.path.realpath(__file__))[0])
    nums=len(Piclist)+5
    RecoveryStr=""
    t_list=[]
    outfile=open(outfile,"wb")
    x=(5,85,165,245,325,405,485,565,645,725,805,885)
    y=(3,83,163,243,323,403,483,563,643,723,803,883)
    for pic in range(nums):    
        src = cv2.imread(str(pic)+'.png')
        if(src is None):
            continue
        datastr="" 
        img=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        img=cv2.blur(img,(3,3))
        thd=cv2.threshold(img,160,255,cv2.THRESH_BINARY)
        for cubes1 in range(1,11):
            datastr+=decode_cube(thd,x[cubes1],y[0])
        for cubes_y in range(1,11):
            for cubes_x in range(12):
                datastr+=decode_cube(thd,x[cubes_x],y[cubes_y])
        for cubes2 in range(1,12):
            datastr+=decode_cube(thd,x[cubes2],y[11])
        nums=int(len(datastr)/8)
        begain=0
        lenth=8
        for i in range(0,nums):
            ch=datastr[begain:lenth]
            t_list.append(ch)
            begain=lenth
            lenth+=8
            outfile.write(struct.pack('B',int(ch,2)))
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

def main(argv):
    VideotoPics(argv[1])
    locim()
    r_list=decode(argv[2])
    fsize=int(os.path.getsize("D:/ct/blist.txt")/8)
    bf=open("D:/ct/blist.txt",'r')
    b_list=[]
    for i in range(fsize):
        b_list.append(bf.read(8))
    valid(b_list,r_list,argv[3])

if __name__ == '__main__':
    main(sys.argv)