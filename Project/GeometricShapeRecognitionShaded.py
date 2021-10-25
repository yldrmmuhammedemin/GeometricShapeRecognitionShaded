import cv2 as cv
import numpy as np
img=cv.imread('ShadedImage.jpeg')
x=int(img.shape[1]*0.5)
y=int(img.shape[0]*0.5)
img=cv.resize(img,(x,y),interpolation=cv.INTER_AREA)
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
meanfilter=cv.blur(gray,(3,3),0)
meanfilter=meanfilter-40
for i in range (0,y):
    for j in range(0,x):
        meanfilter[i,j]=0 if meanfilter[i,j]>=200 else 255
thresh=cv.medianBlur(meanfilter,7)
kernel=np.ones((9,9),np.uint8)
thresh=cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel)
canny = cv.Canny(thresh,200,255)
contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
cv.drawContours(img,contours,-1,(0,255,0),2)
for contour in contours:
    blankimg = np.zeros((img.shape[0], img.shape[1], 3), dtype='uint8')
    blankimg.fill(255)
    cv.drawContours(blankimg, contour, -1, (0, 0, 0), )
    blankimg = cv.cvtColor(blankimg, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(blankimg, 100, 0.4, 10)
    corners = np.int0(corners)
    average = np.average(corners, axis=0)
    average = np.int0(average)
    x ,y = average.ravel()
    fontsize=0.8
    font=cv.FONT_HERSHEY_COMPLEX
    if len(corners) == 3:
      cv.putText(img, "Triangle", (x, y), font, fontsize,(0, 0, 255), 1)
    elif len(corners) == 4:
      cv.putText(img, "Rectangle", (x, y), font, fontsize, (0, 0, 255), 1)
    elif len(corners) == 5:
      cv.putText(img, "Pentagon", (x, y), font, fontsize, (0, 0, 255), 1)
    else:
      cv.putText(img, "Circle", (x, y), font, fontsize, (0, 0, 255), 1)
cv.imshow('GeometricShapeRecognitonShaded',img)
cv.waitKey(0)




