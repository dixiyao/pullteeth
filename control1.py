import math
import socket
import pickle
import time

class tooths(object):
    def __init__(self,points_data):
        self.name = 'name'
        self.levels = points_data[2]
        self.points =points_data[1]
        self.start_point=points_data[0]

with open('data.pkl','rb') as f:
    points_data=pickle.load(f)
t=tooths(points_data)

delegate= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
delegate.connect(('192.168.1.1',30002))
#print("connect success")

#初始点坐标，每次把针头位置设定好以后都要调整
start_x=0.20450
start_y=0.59705
start_z=0.39330
start_rx=3.1044
start_ry=2.1370
start_rz=-0.3580

#以第一个点作为bias校准，如果从第x层开始切，下面的每行第一个中括号里都要改成x
biasx=start_x-t.start_point[0]/1000
biasy=start_y-t.start_point[1]/1000
biasz=start_z-t.start_point[2]/1000

from_start_to_first=[t.start_point]
from_start_to_first.append([t.start_point[0],t.start_point[1],t.start_point[2]-50])
from_start_to_first.append([t.points[0][0][0],t.points[0][0][1],t.start_point[2]-50])
from_start_to_first.append(t.points[0][0])
for p in from_start_to_first:
    x = round(p[0], 2)
    y = round(p[1], 2)
    z = round(p[2], 2)
    x = x / 1000 + biasx
    y = y / 1000 + biasy
    z = z / 1000 + biasz
    command = 'movel(p[' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(start_rx) + ',' + str(start_ry) + ',' + str(
        start_rz) + '],a=0.05, v=0.05, t=0, r=0)\n'

    delegate.send(command.encode("utf8"))
    time.sleep(0.5)

#range( 后数字表示从第x层开始切
for i in range(0,t.levels):
    gogogo = input()
    level=i
    #切除一个平面
    for j in range(0,len(t.points[level])):
        x = round(t.points[level][j][0],2)
        y = round(t.points[level][j][1],2)
        z = round(t.points[level][j][2],2)
        x = x/1000+biasx
        y = y/1000+biasy
        z = z/1000+biasz
        print(x,y,z)
        command='movel(p['+str(x)+','+str(y)+','+str(z)+','+str(start_rx)+','+str(start_ry)+','+str(start_rz)+'],a=0.05, v=0.05, t=0, r=0)\n'
        delegate.send(command.encode("utf8"))
        time.sleep(0.5)
    #移到下一层
    if level==t.levels-1:
        continue
    #同一位置下一层中点
    gogogo=input()
    x = round(t.points[level+1][0][0], 2)
    y = round(t.points[level+1][0][1], 2)
    z = round(t.points[level][-1][2], 2)
    x = x / 1000 + biasx
    y = y / 1000 + biasy
    z = z / 1000 + biasz
    command = 'movel(p[' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(start_rx) + ',' + str(start_ry) + ',' + str(
        start_rz) + '],a=0.05, v=0.05, t=0, r=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(0.5)
    #下一层第一个点
    gogogo = input()
    x = round(t.points[level+1][0][0],2)
    y = round(t.points[level+1][0][1],2)
    z = round(t.points[level+1][0][2],2)
    x = x/1000+biasx
    y = y/1000+biasy
    z = z/1000+biasz
    command = 'movel(p[' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(start_rx) + ',' + str(start_ry) + ',' + str(start_rz) + '],a=0.05, v=0.05, t=0, r=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(0.5)
