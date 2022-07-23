'''
获取图片边界
'''
import cv2
import polyshrink
import numpy as np

def get_estimated_boundary(pic):
    img = cv2.imread(pic)
    # Img2Grey
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Grey2Binary
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 轮廓检测
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
    approx=contours[1]
    c=[[i[0][0]/627,i[0][1]/486] for i in approx]
    #cv2.drawContours(img, contours, 1,(0, 0, 255), 2)
    epsilon = 0.002*cv2.arcLength(contours[1],True)
    approx = cv2.approxPolyDP(contours[1],epsilon,True)
    approx=[[i[0][0]/627,i[0][1]/486] for i in approx]
    # 绘制轮廓
    #cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)
    return c,approx


#def get_estimated_boundary(poly):
#    epsilon = 0.002*cv2.arcLength(approx,True)
#    approx = cv2.approxPolyDP(contours[1],epsilon,True)
if __name__=="__main__":
    get_estimated_boundary(123)
