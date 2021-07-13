'''
TCP 传输控制机械手运动代码
'''
import socket
import pickle
import time

def cut_circle_plane(org_x,org_y,v,knife_r,circle_R,circle_x,circle_y):
    step=2*knife_r
    #模拟切去半径0.05m的⚪面
    #初始点进刀
    
    command='movel(p[-0.39,-0.2,0.4,0,0,0],a=0.01, v=0.01, t=0, r=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(5)
    #第二步，第一圈⚪
    command='movec(p[-0.35,-0.16,0.4,0,0,0],p[-0.31,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(15)
    command='movec(p[-0.35,-0.24,0.4,0,0,0],p[-0.39,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(15)
    #第三步，进一个直径
    command='movel(p[-0.37,-0.2,0.4,0,0,0],a=0.01, v=0.01, t=0, r=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(5)
    #第四步, 第二圈⚪
    command='movec(p[-0.35,-0.18,0.4,0,0,0],p[-0.33,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(10)
    command='movec(p[-0.35,-0.22,0.4,0,0,0],p[-0.37,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
    delegate.send(command.encode("utf8"))
    time.sleep(10)
    #第五步
    command='movel(p[-0.35,-0.2,0.4,0,0,0],a=0.01, v=0.01, t=0, r=0)\n'
    delegate.send(command.encode("utf8"))
    #医生自己控制转
delegate= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
delegate.connect(('192.168.248.140',30002))
'''
command='movel(p[-0.5,-0.4,0.25,0,3,0],a=1.04, v=1.05, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(2)
command='movel(p[-0.3,-0.4,0.25,0,3,0],a=1.04, v=1.05, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(2)
command='movel(p[-0.3,-0.2,0.25,0,3,0],a=1.04, v=1.05, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(2)
command='movel(p[-0.5,-0.2,0.25,0,3,0],a=1.04, v=1.05, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(2)
command='movel(p[-0.5,-0.4,0.25,0,3,0],a=1.04, v=1.05, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(2)
'''
#command='pose=get_actual_tcp_pos()\n'
#command='rrrr = 6666\n'
#command+='textmsg(pose,3)\n'
#delegate.send(command.encode("utf8"))

#模拟切去半径0.05m的⚪面
#初始点进刀
command='movel(p[-0.39,-0.2,0.4,0,0,0],a=0.01, v=0.01, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(5)
#第二步，第一圈⚪
command='movec(p[-0.35,-0.16,0.4,0,0,0],p[-0.31,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(15)
command='movec(p[-0.35,-0.24,0.4,0,0,0],p[-0.39,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(15)
#第三步，进一个直径
command='movel(p[-0.37,-0.2,0.4,0,0,0],a=0.01, v=0.01, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(5)
#第四步, 第二圈⚪
command='movec(p[-0.35,-0.18,0.4,0,0,0],p[-0.33,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(10)
command='movec(p[-0.35,-0.22,0.4,0,0,0],p[-0.37,-0.2,0.4,0,0,0],a=0.01,v=0.01,r=0,mode=0)\n'
delegate.send(command.encode("utf8"))
time.sleep(10)
#第五步
command='movel(p[-0.35,-0.2,0.4,0,0,0],a=0.01, v=0.01, t=0, r=0)\n'
delegate.send(command.encode("utf8"))
#医生自己控制转

'''
command='movel(p[-0.5,-0.4,0.4,0,0,0],a=1.04,v=1.05,t=0,r=0)\n'
delegate.send(command.encode("utf8"))
'''
