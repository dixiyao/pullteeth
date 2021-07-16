import vtk
import matplotlib.pyplot as plt
import numpy as np

#读取stl文件
stlreader=vtk.vtkSTLReader()
stlreader.SetFileName(r"C:\Users\Administrator\Desktop\Tooth\GetPoint2\Segmentation_Segment_1.stl")
stlreader.Update()

#根据测试，x轴为牙齿长轴，故沿y轴逆时针旋转90°
rotate1=vtk.vtkTransform()
rotate1.RotateY(-90)
filter1=vtk.vtkTransformPolyDataFilter()
filter1.SetInputConnection(stlreader.GetOutputPort())
filter1.SetTransform(rotate1)
filter1.Update()

#旋转后的结果写入result.stl文件
stlwriter=vtk.vtkSTLWriter()
stlwriter.SetFileName(r"C:\Users\Administrator\Desktop\Tooth\GetPoint2\result.stl")
stlwriter.SetInputConnection(filter1.GetOutputPort())
stlwriter.Write()

#获取点坐标，按z值划分XOY平面，间隔为2mm。
p=[0,0,0]
polydata=filter1.GetOutput()
points=[]
new_z=[]
file=open(r"C:\Users\Administrator\Desktop\Tooth\GetPoint2\data.txt",mode="w")
for i in range(polydata.GetNumberOfPoints()):
    polydata.GetPoint(i,p)
    z=int(p[2])
    if p[2]-z<0 and z%2==1:
        z=z-1
    if p[2]-z>=0 and z%2==1:
        z=z+1 
    if (z not in new_z):
        new_z.append(z)
#逆序排列，表面的牙z值大
new_z.sort(reverse=True)
for i in range(0,len(new_z)):
    tmp=[]
    points.append(tmp)
for i in range(polydata.GetNumberOfPoints()):
    polydata.GetPoint(i,p)
    z=int(p[2])
    if p[2]-z<0 and z%2==1:
        z=z-1
    if p[2]-z>=0 and z%2==1:
        z=z+1
    index=new_z.index(z)
    tmp=[p[0],p[1],p[2]]
    points[index].append(tmp)
# for i in range(0,len(points)):
#     file.write(str(new_z[i])+":  "+str(len(points[i]))+"\n")
#     for j in range(0,len(points[i])):
#         file.write(str(round(points[i][j][0],2))+" "+str(round(points[i][j][1],2))+" "+str(round(points[i][j][2],2))+'\n')
#     file.write("\n")

#修改获取哪一层的数据
level=1
for i in range(0,len(points[level])):
    file.write(str(round(points[level][i][0],2))+" "+str(round(points[level][i][1],2))+" "+str(round(points[level][i][2],2))+'\n')
