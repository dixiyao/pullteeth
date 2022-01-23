import numpy as np
import copy
import socket
import time
import icp
from icp import jaw_and_tooth
import struct
import pickle

import open3d as o3d

class jaw_and_robot(jaw_and_tooth):
    def __init__(self,jawname,single_tooth=False):
        jaw_and_tooth.__init__(self,jawname,jawname,single_tooth)
        self.jawname=jawname

    def transform_to_robot(self,robotpoints):
        self.robot =copy.deepcopy(self.jaw)
        self.robot.points = o3d.utility.Vector3dVector(robotpoints)
        self.robot.paint_uniform_color([0,1.0,0])
        self.jaw.points = o3d.io.read_triangle_mesh(self.jawname + '.stl').vertices
        #o3d.visualization.draw_geometries([self.robot,self.tooth,self.jaw])
        threshold = 10000.0  # 移动范围的阀值
        trans_init = np.asarray([[1, 0, 0, 0],  # 4x4 identity matrix，这是一个转换矩阵，
                                 [0, 1, 0, 0],  # 象征着没有任何位移，没有任何旋转，我们输入
                                 [0, 0, 1, 0],  # 这个矩阵为初始变换
                                 [0, 0, 0, 1]])

        # 运行icp
        reg_p2p = o3d.pipelines.registration.registration_icp(
            self.jaw, self.robot, threshold, trans_init,
            o3d.pipelines.registration.TransformationEstimationPointToPoint())
        R = np.matrix(reg_p2p.transformation)
        A = R#.I
        print(A)
        self.jaw.transform(A)
        o3d.visualization.draw_geometries([self.robot,self.jaw])

class jaw_and_tooth_and_robot(jaw_and_tooth):
    def __init__(self,toothname,jawname,single_tooth=False):
        jaw_and_tooth.__init__(self,toothname,jawname,single_tooth)

    def transform_to_robot(self,robotpoints):
        print(np.asarray(self.jaw.points))
        self.robot =copy.deepcopy(self.jaw)
        self.robot.points = o3d.utility.Vector3dVector(robotpoints)
        self.robot.paint_uniform_color([0,1.0,0])
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
        for i in range(level):
            this_heights=[]
            for ind in index[i]:
                this_heights.append(points[ind])
            remove_points.append(this_heights)
        cx = [x[0] for x in remove_points[0]]
        cy = [x[1] for x in remove_points[0]]
        cz = [x[2] for x in remove_points[0]]
        start = [np.mean(np.array(cx)), np.mean(np.array(cy)), np.mean(np.array(cz))]

        return start, remove_points, level

#配准牙齿，头骨，还有在头骨上用机械手划出来reg.pkl的点三位一体
if __name__=='__main__':
    with open('get2.pkl', 'rb') as f:
        registration_points=pickle.load(f)
    triple = jaw_and_robot('2', False)
    robots = np.array(registration_points)*1000

    # planereversepoints=triple.plane_detection_transform()
    # remove_points_index,level=triple.getremovepoints_index(planereversepoints)

    triple.transform_to_robot(robots)
    # points = triple.getpoints(istooth=True)
    # start, removepoints, level = triple.getremovepoints_byindex(points,remove_points_index,level)
    #
    # with open('data.pkl','wb') as f:
    #     pickle.dump((start,removepoints,level),f)


