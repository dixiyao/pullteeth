import copy
import math
import pickle
from sklearn.preprocessing import normalize

import open3d as o3d
import vtk
import numpy as np
import matplotlib.pyplot as plt

from Errors import*

#读取电脑中的 ply 点云文件
def read_ply_from_stl(name):
    stlreader=vtk.vtkSTLReader()
    stlreader.SetFileName(name+'.stl')
    stlreader.Update()

    rotate1 = vtk.vtkTransform()
    #rotate1.RotateX(180)
    #rotate1.RotateY(180)
    filter1 = vtk.vtkTransformPolyDataFilter()
    filter1.SetInputConnection(stlreader.GetOutputPort())
    filter1.SetTransform(rotate1)
    filter1.Update()

    plyWriter=vtk.vtkPLYWriter()
    plyWriter.SetFileName(name+'.ply')
    plyWriter.SetInputConnection(filter1.GetOutputPort())
    plyWriter.Write()

    source = o3d.io.read_point_cloud(name+'.ply')

    return source

class jaw_and_tooth():
        def __init__(self,toothname,jawname,single_tooth=False):
            self.singletooth=single_tooth

            tooth=o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.asarray(o3d.io.read_triangle_mesh(toothname + '.stl').vertices)))
            #tooth=tooth.voxel_down_sample(voxel_size=0.01)
            jaw=o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.asarray(o3d.io.read_triangle_mesh(jawname + '.stl').vertices)))
            #jaw=jaw.voxel_down_sample(voxel_size=0.01)

            #为两个点云上上不同的颜色
            tooth.paint_uniform_color([1, 0.706, 0])    #source 为黄色
            jaw.paint_uniform_color([0, 0.651, 0.929])#target 为蓝色

            if not single_tooth==True:
            #icp配准
                threshold = 100.0  #移动范围的阀值
                trans_init = np.asarray([[1,0,0,0],   # 4x4 identity matrix，这是一个转换矩阵，
                                         [0,1,0,0],   # 象征着没有任何位移，没有任何旋转，我们输入
                                         [0,0,1,0],   # 这个矩阵为初始变换
                                         [0,0,0,1]])

                #运行icp
                reg_p2p = o3d.pipelines.registration.registration_icp(
                        tooth, jaw, threshold, trans_init,
                        o3d.pipelines.registration.TransformationEstimationPointToPoint())

                #将我们的矩阵依照输出的变换矩阵进行变换
                print(reg_p2p)
                tooth.transform(reg_p2p.transformation)

            self.tooth=tooth
            self.jaw=jaw

        #获取牙齿点云坐标
        def getpoints(self,istooth=True):
            if istooth:
                pointarray=np.array(self.tooth.points)
            else:
                pointarray=np.array(self.jaw.points)

            return pointarray

        #heightlevel为每层高度
        #获取要切除的点坐标格式，也就是牙齿，但是是按层划分的格式
        def getremovepoints(self,points,height_level = 1):
            points=np.array(points)
            x = []
            y = []
            z = []
            for p in points:
                x.append(p[0])
                y.append(p[1])
                z.append(p[2])
            print(max(x),min(x),max(y),min(y),max(z),min(z))
            remove_points = []
            level = 0
            current_height = max(z)
            while current_height >min(z):
                thisheight = []
                for i in range(len(z)):
                    if (z[i] > current_height-height_level and z[i] <= current_height ):
                        thisheight.append([x[i], y[i], z[i]])
                remove_points.append(thisheight)
                level += 1
                current_height -= height_level  # 层高1mm

            #找start point,第一层的中心
            cx=[x[0] for x in remove_points[0]]
            cy = [x[1] for x in remove_points[0]]
            cz = [x[2] for x in remove_points[0]]
            start=[np.mean(np.array(cx)),np.mean(np.array(cy)),np.mean(np.array(cz))]

            return start,remove_points,level

        #通过交互式界面由医生选择坐标的三个方向
        #例如x轴，先选x1,再选x2，正方向为x1 to x2
        #三个轴选完选择起始点
        def select_ref(self):
            vis = o3d.visualization.VisualizerWithEditing()
            vis.create_window()

            # 将两个点云放入visualizer
            vis.add_geometry(self.tooth)

            # 让visualizer渲染点云
            vis.update_geometry()
            vis.poll_events()
            vis.update_renderer()

            vis.run()
            vis.destroy_window()
            x1, x2, y1, y2, z1, z2, s = vis.get_picked_points()

            return x1,x2,y1,y2,z1,z2,s

        #依照选取的参考轴，旋转图片确定方向，这一步重要
        #可能再实时确定方向的时候需要使用
        def transform_axis(self,x1,x2,y1,y2,z1,z2,s):
            points = self.getpoints(istooth=False)
            xi = points[x2] - points[x1]
            yj = points[y2] - points[y1]
            zk = points[z2] - points[z1]
            e = [xi, yj, zk]
            e = np.array(e)
            e = normalize(e, axis=1, norm='l2')
            start = points[s]

            points = self.getpoints(istooth=True)
            for i in range(points.shape[0]):
                p = np.dot(e, points[i])
                points[i] = p
            start = np.dot(e, np.array(start))

            return points,start

        def plane_detection_transform(self):
            # if self.singletooth==False:
            #    raise PlaneErorr

            plane_model, inliers = self.tooth.segment_plane(distance_threshold=0.01,
                                                     ransac_n=5,
                                                     num_iterations=1000)
            [a, b, c, d] = plane_model
            print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

            #rotation matrix
            norm=math.sqrt(a*a+b*b+c*c)
            a=a/norm
            b=b/norm
            c=c/norm
            beta=math.asin(a)
            sinalpha=-b/math.cos(beta)
            alpha=math.asin(sinalpha)
            X=np.matrix([[1,0,0,0],
                         [0,math.cos(alpha),-math.sin(alpha),0],
                         [0,math.sin(alpha),math.cos(alpha),0],
                         [0,0,0,1]])
            Y = np.matrix([[math.cos(beta),0,math.sin(beta),0],
                           [0, 1,0,0],
                           [-math.sin(beta),0,math.cos(beta),0],
                           [0, 0, 0, 1]])
            Z = np.matrix([[1,0,0,0],
                           [0, 1,0, 0],
                           [0, 0,1, 0],
                           [0, 0, 0, 1]])
            R =np.dot(np.dot(X,Y),Z)
            A =R.I
            A  =A[:3,:3]
            A = A.T

            points=np.array(self.tooth.points)
            xyz=np.dot(np.mat(points),A)

            # new=copy.deepcopy(self.tooth)
            # new.points=o3d.utility.Vector3dVector(xyz)
            # new.paint_uniform_color([0,1,0])
            # o3d.visualization.draw_geometries([self.tooth,new])

            if self.singletooth==True:
                self.tooth.points=o3d.utility.Vector3dVector(xyz)

            return xyz


        def visualize(self):
            draw=[self.tooth]
            # 将两个点云放入visualizer
            if not self.singletooth==True:
                draw.append(self.jaw)
            o3d.visualization.draw_geometries(draw)

        def chooseref(self):
            vis = o3d.visualization.VisualizerWithEditing()
            vis.create_window()

            # 将两个点云放入visualizer
            vis.add_geometry(self.jaw)
            vis.add_geometry(self.tooth)

            # 让visualizer渲染点云
            vis.update_geometry()
            vis.poll_events()
            vis.update_renderer()

            vis.run()
            vis.destroy_window()
            choosepoints= vis.get_picked_points()
            points = self.getpoints(istooth=False)
            return np.mat([points[p] for p in choosepoints])

def draw3D(points,start):
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    # 定义图像和三维格式坐标轴
    fig = plt.figure()
    ax2 = Axes3D(fig)
    xd = [a[0] for a in points]
    yd = [a[1] for a in points]
    zd = [a[2] for a in points]
    ax2.scatter3D(xd,yd,zd, cmap='Blues')
    ax2.scatter3D([start[0]],[start[1]],[start[2]],cmap='Red')
    plt.show()

#配准牙齿和头骨的pair
if __name__=='__main__':
    print(o3d.__version__)
    pair=jaw_and_tooth('21','head',True)
    pair.plane_detection_transform()
    points = pair.getpoints(istooth=True)
    start, removepoints, level = pair.getremovepoints(points)
    draw3D(points,start)
    pair.visualize()
#生成路径
    with open('data.pkl','wb') as f:
        pickle.dump((start,removepoints,level),f)
