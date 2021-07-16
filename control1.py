import socket
import pickle
import time

delegate= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
delegate.connect(('169.254.174.11',30002))
print("connect success")

data=open('data.txt')
data=data.readlines()
start_x=-0.39816
start_y=-0.43976
start_z=0.0638+0.4
biasx=start_x+0.02557
biasy=start_y-0.08304
biasz=start_z-0.06501
for line in data:
    lines=line.split(' ')
    x = float(lines[0])
    y = float(lines[1])
    z = float(lines[2])
    x = x/1000+biasx
    y = y/1000+biasy
    z = z/1000+biasz
    print(x,y,z)
    command='movel(p['+str(x)+','+str(y)+','+str(z)+','+'0,0,0],a=0.01, v=0.05, t=0, r=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(0.05)