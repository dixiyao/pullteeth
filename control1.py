import socket
import pickle
import time
from read_data import tooth

t=tooth(r'T T_Green_Split_002.stl')
t.transform_reverse_up_and_down()
delegate= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
delegate.connect(('169.254.174.11',30002))
print("connect success")

#初始点坐标
start_x=-0.16477
start_y=-0.53254
start_z=-0.24378+0.4
start_rx=2.3499
start_ry=-3.0351
start_rz=-3.1150
biasx=start_x-t.points[0][0][0]/1000
biasy=start_y-t.points[0][0][1]/1000
biasz=start_z-t.points[0][0][2]/1000

for i in range(t.levels):
    level=i
    #t.get_level(i+1)
    #data=open('data.txt')
    #data=data.readlines()
    #切除一个平面
    for j in range(0,len(t.points[level])):
        x = round(t.points[level][j][0],2)
        y = round(t.points[level][j][1],2)
        z = round(t.points[level][j][2],2)
        x = x/1000+biasx
        y = y/1000+biasy
        z = z/1000+biasz
        print(x,y,z)
        command='movel(p['+str(x)+','+str(y)+','+str(z)+','+str(start_rx)+','+str(start_ry)+','+str(start_rz)+'],a=0.01, v=0.05, t=0, r=0)\n'
        #delegate.send(command.encode("utf8"))
        time.sleep(0.05)
    #移到下一层
    if level==t.levels-1:
        continue
    x = round(t.points[level+1][0][0],2)
    y = round(t.points[level+1][0][1],2)
    z = round(t.points[level+1][0][2],2)
    x = x/1000+biasx
    y = y/1000+biasy
    z = z/1000+biasz
    command = 'movel(p[' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(start_rx) + ',' + str(start_ry) + ',' + str(start_rz) + '],a=0.01, v=0.05, t=0, r=0)\n'
    #delegate.send(command.encode("utf8"))
    time.sleep(0.05)
