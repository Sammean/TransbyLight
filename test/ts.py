import numpy as np
import cv2
from PIL import Image
import os
Piclist = os.listdir("D:/test/tt/")
for pic in Piclist:
    if pic.endswith(".png"): 
        image_path="D:/test/tt/"+pic
        src=cv2.imread(image_path)
        gray=cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        gradX = cv2.Sobel(gray, cv2.CV_32F, 1, 0,-1)
        gradY = cv2.Sobel(gray, cv2.CV_32F, 0, 1,-1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 0,255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        closed = cv2.erode(closed, None, iterations = 4)
        closed = cv2.dilate(closed, None, iterations = 4)
        cnts,hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))
        area=(box[3][1],box[1][0],box[0][0],box[1][1])
        img=Image.open(image_path)
        cropped = img.crop(area)
        cropped.show()

