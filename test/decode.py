import cv2
from PIL import Image
import numpy as np
import math

def Center_cal(contours,i):
    n=len(contours[i])
    centerx = (contours[i][n/4].x + contours[i][n * 2 / 4].x + contours[i][3 * n / 4].x + contours[i][n - 1].x) /4
    centery = (contours[i][n/4].y + contours[i][n * 2 / 4].y + contours[i][3 * n / 4].y + contours[i][n - 1].y) /4
    point=(cenrerx,centery)
    return point

#图像处理
src=cv2.imread("D:/test/tt/6.png")
cv2.imshow("src",src)
cv2.waitKey(0)
gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
blured=cv2.blur(gray,(3,3))
src2=cv2.equalizeHist(blured)
cv2.imshow("lv bo",src2)
cv2.waitKey(0)
thresh= cv2.threshold(src2, 112,255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)
contours,hierarchy=cv2.findContours(colsed.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#筛选
ic=0
parentIdx=-1
contours2=[]
for i in range(len(contours)):
    if(hierarchy[i][2]!=-1&ic==0):
        parentIdx=i
        ic+=1
    elif(hierarchy[i][2]!=-1):
        ic+=1
    elif(hierarchy[i][2]==-1):
        ic=0
        parentIdx=-1
    if(ic>=2):
        contours2.append(contours[parentIdx])
        ic=0
        parentIdx=-1
        area=cv2.contourArea(contours[i])


for i in range(len(contours2)):
    point[i]=Center_cal(contours2,i)
    
area=cv2.contourArea(contours2[1])
area_side=round(math.sqrt(area))
for i in range(len(contours2)):
    dst=cv2.line(point[i%len(contours2)],point[(i+1)%len(contours2)],cv2.PARAM_SCALAR(20,21,237),3)
cv2.imshow("erwei",dst)