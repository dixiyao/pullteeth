import numpy as np
import copy
from icp import jaw_and_tooth
import pickle

import open3d as o3d

class jaw_and_robot(jaw_and_tooth):
    def __init__(self,jawname,single_tooth=False):
        jaw_and_tooth.__init__(self,jawname,jawname,single_tooth)
        self.jawname=jawname

    def transform_to_robot(self,robotpoints):
        self.robot =copy.deepcopy(self.jaw)
        self.robot.points = o3d.utility.Vector3dVector(robotpoints)
        self.robot.paint_uniform_color([1, 0.706, 0])
        self.jaw.points = o3d.io.read_triangle_mesh(self.jawname + '.stl').vertices
        #o3d.visualization.draw_geometries([self.robot,self.tooth,self.jaw])
        threshold = 10000.0  # 移动范围的阀值
        trans_init = np.asarray([[1, 0, 0, 0],  # 4x4 identity matrix，这是一个转换矩阵，
                                 [0, 1, 0, 0],  # 象征着没有任何位移，没有任何旋转，我们输入
                                 [0, 0, 1, 0],  # 这个矩阵为初始变换
                                 [0, 0, 0, 1]])

        # 运行icp
        reg_p2p = o3d.pipelines.registration.registration_icp(
            self.robot, self.jaw, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())
        R = np.matrix(reg_p2p.transformation)
        A = R.I
        print(A)
        self.jaw.transform(A)
        o3d.visualization.draw_geometries([self.robot,self.jaw])
        for r in self.robot.points:
            minx=10000
            for j in self.jaw.points:
                d=np.sqrt(np.sum(r-j))
                minx=min(minx,d)
            print(minx)

class jaw_and_tooth_and_robot(jaw_and_tooth):
    def __init__(self,toothname,jawname,single_tooth=False):
        jaw_and_tooth.__init__(self,toothname,jawname,single_tooth)

    def transform_to_robot(self,robotpoints):
        print(np.asarray(self.jaw.points))
        self.robot =copy.deepcopy(self.jaw)
        self.robot.points = o3d.utility.Vector3dVector(robotpoints)
        self.robot.paint_uniform_color([1, 0.706, 0])
        #o3d.visualization.draw_geometries([self.robot,self.tooth,self.jaw])
        threshold = 10000.0  # 移动范围的阀值
        trans_init = np.asarray([[1, 0, 0, 0],  # 4x4 identity matrix，这是一个转换矩阵，
                                 [0, 1, 0, 0],  # 象征着没有任何位移，没有任何旋转，我们输入
                                 [0, 0, 1, 0],  # 这个矩阵为初始变换
                                 [0, 0, 0, 1]])

        # 运行icp
        reg_p2p = o3d.pipelines.registration.registration_icp(
            self.robot,self.jaw , threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())
        R = np.matrix(reg_p2p.transformation)
        A = R.I
        print(A)
        self.tooth.transform(A)
        self.jaw.transform(A)
        o3d.visualization.draw_geometries([self.robot,self.jaw,self.tooth])


    def getremovepoints_index(self, points, height_level=1):
        points = np.array(points)
        x = []
        y = []
        z = []
        for p in points:
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])
        remove_points_index = []
        level = 0
        current_height = max(z)
        while current_height > min(z):
            thisheight = []
            for i in range(len(z)):
                if (z[i] > current_height - height_level and z[i] <= current_height):
                    thisheight.append(i)
            remove_points_index.append(thisheight)
            level += 1
            current_height -= height_level  # 层高1mm

        return remove_points_index,level

    def getremovepoints_byindex(self,points,index,level):
        remove_points=[]
        xx = []
        yy = []
        zz = []
        for i in range(level):
            this_heights=[]
            x = []
            y = []
            for ind in index[i]:
                this_heights.append(points[ind])
                xx.append(points[ind][0])
                yy.append(points[ind][1])
                zz.append(points[ind][2])
                x.append(points[ind][0])
                y.append(points[ind][1])
            # import matplotlib.pyplot as plt
            # plt.title(i+1)
            # plt.plot(x,y)
            # plt.show()
            # remove_points.append(this_heights)
            # print(zz[-1])
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        # 定义图像和三维格式坐标轴
        fig = plt.figure()
        ax2 = Axes3D(fig)
        ax2.scatter3D(xx, yy, zz, cmap='Blues')
        plt.show()

        cx = [x[0] for x in remove_points[0]]
        cy = [x[1] for x in remove_points[0]]
        cz = [x[2] for x in remove_points[0]]
        start = [np.mean(np.array(cx)), np.mean(np.array(cy)), np.mean(np.array(cz))]

        return start, remove_points, level

# 从人为给定的一个平面，已经在牙齿上做好平面，平面可以倾斜放置，每层切削去一个改平面平行面，此方法叫 PlaneInitialize
def PlaneInitialize(robots,triple):
    planereversepoints=triple.plane_detection_transform() # for PlaneInitialize
    remove_points_index,level=triple.getremovepoints_index(planereversepoints) # for PlaneInitialize
    triple.transform_to_robot(robots)
    points = triple.getpoints(istooth=True)
    start, removepoints, level = triple.getremovepoints_byindex(points, remove_points_index, level)

    return start,removepoints,level

# 无法在图像上找到平面，仅从当前放置方法找一个最高点，每次切削去一个水平平面，此方法叫PointInitialize
def PointInitialize(robots,triple):
    triple.transform_to_robot(robots)
    points = triple.getpoints(istooth=True)
    remove_points_index, level = triple.getremovepoints_index(points)
    start, removepoints, level = triple.getremovepoints_byindex(points,remove_points_index,level)

    return start, removepoints, level

# 配准牙齿，头骨，还有在头骨上用机械手划出来reg.pkl的点三位一体
if __name__=='__main__':
    with open('data.pkl', 'rb') as f:
        registration_points=pickle.load(f)
    print(registration_points)
    #triple = jaw_and_robot('3', False)
    triple  = jaw_and_tooth_and_robot('44','44',False)
    robots = np.array(registration_points)*1000

    start,removepoints,level=PointInitialize(robots,triple)#PlaneInitialize(robots,triple)
    #
    with open('route.pkl','wb') as f:
         pickle.dump((start,removepoints,level),f)


