import vtk
import matplotlib.pyplot as plt
import numpy as np
import copy
import math

class tooth(object):
    def __init__(self,name):
        self.name=name
        #读取stl文件
        stlreader=vtk.vtkSTLReader()
        stlreader.SetFileName(name)
        stlreader.Update()

        
        #根据测试，x轴为牙齿长轴，故沿y轴逆时针旋转90°
        rotate1=vtk.vtkTransform()
        #rotate1.RotateY(-90)
        filter1=vtk.vtkTransformPolyDataFilter()
        filter1.SetInputConnection(stlreader.GetOutputPort())
        filter1.SetTransform(rotate1)
        filter1.Update()
        
        #旋转后的结果写入result.stl文件
        stlwriter=vtk.vtkSTLWriter()
        stlwriter.SetFileName(r"result.stl")
        stlwriter.SetInputConnection(filter1.GetOutputPort())
        stlwriter.Write()
        
        #获取点坐标，按z值划分XOY平面，间隔为2mm。
        p=[0,0,0]
        polydata=filter1.GetOutput()
        points=[]
        new_z=[]
        
        for i in range(polydata.GetNumberOfPoints()):
            polydata.GetPoint(i,p)
            z=int(p[2])
            if p[2]-z<0 and z%2==1:
                z=-z-0.5
            if p[2]-z>=0 and z%2==1:
                z=z+0.5
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
                z=z-0.5
            if p[2]-z>=0 and z%2==1:
                z=z+0.5
            index=new_z.index(z)
            tmp=[p[0],p[1],p[2]]
            points[index].append(tmp)
        # for i in range(0,len(points)):
        #     file.write(str(new_z[i])+":  "+str(len(points[i]))+"\n")
        #     for j in range(0,len(points[i])):
        #         file.write(str(round(points[i][j][0],2))+" "+str(round(points[i][j][1],2))+" "+str(round(points[i][j][2],2))+'\n')
        #     file.write("\n")

        for i in range(len(points)):
            temp=[[points[i][0][0],points[i][0][1],points[i][0][2]]]
            for j in range(len(points[i])-1):
                x = points[i][j][0]
                y = points[i][j][1]
                z = points[i][j][2]
                x_ = points[i][j+1][0]
                y_ = points[i][j+1][1]
                z_ = points[i][j+1][2]
                dis=math.sqrt((x-x_)*(x-x_)+(y-y_)*(y-y_)+(z-z_)*(z-z_))
                if dis>1:
                    temp.append([x_,y_,z_])
            points[i]=temp

        self.points=points
        self.levels=len(points)

    def transform_reverse_up_and_down(self):
        points_bk=copy.deepcopy(self.points)
        for i in range(len(self.points)):
            self.points[i]=points_bk[len(self.points)-i-1]

    def transform_z_negetive(self):
        for j in range(len(self.points)):
            for i in range(len(self.points[j])):
                self.points[j][i][2]=-self.points[j][i][2]
        
    def get_level(self,level):
        points=self.points
        file=open(r"data.txt",mode="w")
        #修改获取哪一层的数据
        level=1
        for i in range(0,len(points[level])):
            file.write(str(round(points[level][i][0],2))+" "+str(round(points[level][i][1],2))+" "+str(round(points[level][i][2],2))+'\n')

    def draw_level(self,level):
        x=[]
        y=[]
        for i in range(0,len(self.points[level])):
            x.append(self.points[level][i][0])
            y.append(self.points[level][i][1])
        plt.scatter(x,y,color='blue')
        plt.scatter([self.points[level][0][0]],[self.points[level][0][1]],color='red')
        plt.show()

if __name__=="__main__":
    t=tooth(r"T T_Green_Split_002.stl")
    t.get_level(0)
    t.transform_reverse_up_and_down()
    for i in range(t.levels):
        print(t.points[i][0][2])

        
