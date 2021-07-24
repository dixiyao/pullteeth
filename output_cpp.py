import math
import socket
import pickle
import time
from read_data import tooth

t=tooth(r'T T_Green_Split_002.stl')
### 注释下面两行，则为反向
t.transform_reverse_up_and_down()
t.transform_z_negetive()
'''
#初始点坐标，每次把针头位置设定好以后都要调整
start_x=-0.21488
start_y=-0.76436
start_z=0.49784
start_rx=0.7106
start_ry=3.0611
start_rz=-1.2311
#以第一个点作为bias校准，如果从第x层开始切，下面的每行第一个中括号里都要改成x
biasx=start_x-t.points[0][0][0]/1000
biasy=start_y-t.points[0][0][1]/1000
biasz=start_z-t.points[0][0][2]/1000
'''

data=open('up2down.txt','w')
#range( 后数字表示从第x层开始切
for i in range(0,t.levels):
    level=i
    for j in range(0,len(t.points[level])):
        x = round(t.points[level][j][0],2)
        y = round(t.points[level][j][1],2)
        z = round(t.points[level][j][2],2)
        x = x/1000
        y = y/1000
        z = z/1000
        data.write(str(x)+' '+str(y)+' '+str(z)+'\n')
    #移到下一层
    if level==t.levels-1:
        continue
    x = round(t.points[level+1][0][0], 2)
    y = round(t.points[level+1][0][1], 2)
    z = round(t.points[level][-1][2], 2)
    x = x / 1000
    y = y / 1000
    z = z / 1000
    data.write(str(x)+' '+str(y)+' '+str(z)+'\n')
    #下一层第一个点
    x = round(t.points[level+1][0][0],2)
    y = round(t.points[level+1][0][1],2)
    z = round(t.points[level+1][0][2],2)
    x = x/1000
    y = y/1000
    z = z/1000
    data.write(str(x)+' '+str(y)+' '+str(z)+'\n')