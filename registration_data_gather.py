import socket
import winsound
import struct
import pickle

def prepare(s):
    packet_1 = s.recv(4)
    packet_2 = s.recv(8)
    packet_3 = s.recv(48)
    packet_4 = s.recv(48)
    packet_5 = s.recv(48)
    packet_6 = s.recv(48)
    packet_7 = s.recv(48)
    packet_8 = s.recv(48)
    packet_9 = s.recv(48)
    packet_10 = s.recv(48)
    packet_11 = s.recv(48)

def get_registration_point(samples=500):
    print("敲回车开始")
    go=input()
    #获取点
    registration_points=[]
    for i in range(samples):
        delegate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        delegate.connect(('169.254.1.3', 30003))
        prepare(delegate)
        packet = delegate.recv(8)
        x = struct.unpack('!d', packet)[0]
        packet = delegate.recv(8)
        y = struct.unpack('!d', packet)[0]
        packet = delegate.recv(8)
        z = struct.unpack('!d', packet)[0]
        packet = delegate.recv(8)
        rx = struct.unpack('!d', packet)[0]
        packet = delegate.recv(8)
        ry = struct.unpack('!d', packet)[0]
        packet = delegate.recv(8)
        rz = struct.unpack('!d', packet)[0]
        print(i,x,y,z,rx,ry,rz)
        registration_points.append([x,y,z])
        winsound.Beep(440, 500)
        gogogo=input()
        delegate.close()

    return registration_points

if __name__=='__main__':
    registration_points=get_registration_point(50)
    with open('data.pkl', 'wb') as f:
       pickle.dump(registration_points,f)
    with open('data.pkl', 'rb') as f:
        registration_points=pickle.load(f)
    for point in registration_points:
        print(point)

