from cmath import sqrt
import math
import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

class tooths(object):
    def __init__(self, points_data):
        self.name = 'name'
        self.levels = points_data[2] # 层数
        self.points = points_data[1]
        self.start_point = points_data[0]

'''
    BasicRoutine和CoverageRoutine为具体的路径规划算法实现
'''

class Routine(object):
    def __init__(self, tooth):
        self.tooth = tooth
        self.routine = self.getRoutine()
        self.length = self.getLength()
    
    def getRoutine(self):
        raise NotImplementedError
    
    def getLength(self):
        total_length = 0
        for i in range(0, np.shape(self.routine)[0]):
            length = 0
            for j in range(1, len(self.routine[i])):
                length = length + math.sqrt(math.pow(self.routine[i][j-1][0] - self.routine[i][j][0], 2) + math.pow(self.routine[i][j-1][1] - self.routine[i][j][1], 2))
            print("Level %d routine length: %f" % (i, length))
            total_length = total_length + length
        return total_length
    
    def visualizePoints(self):
        # 设置刻度间隔
        x_major_locator=MultipleLocator(1)
        y_major_locator=MultipleLocator(1)
        for i in range(0, np.shape(self.routine)[0]):
            X = []
            Y = []
            for j in range(0, len(self.routine[i])):
                X.append(self.routine[i][j][0])
                Y.append(self.routine[i][j][1])
            plt.scatter(X, Y, color='red', marker='+')
            ax = plt.gca()
            ax.xaxis.set_major_locator(x_major_locator)
            ax.yaxis.set_major_locator(y_major_locator)
            plt.grid()
            plt.show()
    
    def visualizeRoutine(self):
        return NotImplementedError

''' 
    将所有数据点按顺序连起来的路径
    可作为Baseline
'''

class BasicRoutine(Routine):
    def __init__(self, tooth):
        super().__init__(tooth)

    def getRoutine(self):
        return self.tooth.points
    
    def getLength(self):
        return super().getLength()
    
    def visualizePoints(self):
        super().visualizePoints()

    def visualizeRoutine(self):
        # 设置刻度间隔
        x_major_locator=MultipleLocator(1)
        y_major_locator=MultipleLocator(1)
        for i in range(0, np.shape(self.routine)[0]):
            X = []
            Y = []
            for j in range(0, len(self.routine[i])):
                X.append(self.routine[i][j][0])
                Y.append(self.routine[i][j][1])
                if j != 0:
                    plt.plot([self.routine[i][j-1][0], self.routine[i][j][0]], [self.routine[i][j-1][1], self.routine[i][j][1]], color = 'lightblue', linewidth = 0.3)
            plt.scatter(X, Y, color='red', marker='+')
            ax = plt.gca()
            ax.xaxis.set_major_locator(x_major_locator)
            ax.yaxis.set_major_locator(y_major_locator)
            plt.grid()
            plt.show()

'''
    优化路径: 平面覆盖法
    1.以z轴将三维模型划分成若干牙齿平面(registration.py中已完成)
    2.对每个平面划分成若干d*d矩形网格(square), 以灰色可视化
    3.将散点置入网格中, 以红色可视化
    4.取每一列最外的两个点连成路径, 构成外围轮廓(self.boundary), 以浅蓝色可视化
    5.判定哪些网格中心需要被覆盖(由于磨削工具本身具有直径, 经过网格中心即说明网格区域被覆盖), 以绿色可视化
    6.将这些网格中心按顺序连接即得到路径routine, 以绿色可视化

    说明:
    1. 网格大小等于磨削工具的直径; 可以修改, 但需要考虑刀具能覆盖多少网格的问题
    2. 刀具的覆盖范围是一个圆, 需要考虑网格的四个角
    3. 算法还有很多需要完善的地方：
        - 数据点分布在外围，内部部分网格没有数据点，用“周围四个网格有数据点”判定网格需要覆盖会导致缺失。所以后面几个结果图的路径会缺失
        可能的解决方案: 从每个网格中心出发, 沿x和y正负方向作射线, 与第四步求得的boundary相交. x和y正负方向分别有且仅有一个交点则说明在内部, 根据距离判断路径是否应经过
        - boundary出现凹陷(图上表现为尖角), 同样是因为数据点分散的问题. 可以考虑删除斜率过大的点对应的线段, 因为通常情况下牙齿截面应该是相对较为规则的多边形
        - 路径直接将需要覆盖的网格点相连. 不是最短距离, 可以优化, 但差距不大.
'''

class CoverageRoutine(Routine):
    def __init__(self, tooth):
        super().__init__(tooth)

    def getRoutine(self):
        d = 1   # 划分网格单位距离
        self.boundary = [[] for i in range(0, self.tooth.levels)] # 模拟牙齿平面最外层的轮廓，第一维是以2mm为厚度进行平面划分，后两维是每一层上的边界点
        routine = [[] for i in range(0, self.tooth.levels)] # 最终路径，同上划分为三维
        for i in range(0, len(self.boundary)):
            # 获取散点图范围
            x_min = x_max = self.tooth.points[i][0][0]
            y_min = y_max = self.tooth.points[i][0][1]
            for point in self.tooth.points[i]:
                x_min = point[0] if point[0] < x_min else x_min
                x_max = point[0] if point[0] > x_max else x_max
                y_min = point[1] if point[1] < y_min else y_min
                y_max = point[1] if point[1] > y_max else y_max
            x_min = math.floor(x_min)
            x_max = math.ceil(x_max)
            y_min = math.floor(y_min)
            y_max = math.ceil(y_max)
            # 创建网格square，根据网格单元的宽度d确定网格的数量，square从左下角开始（square[0][0]），x增大向右，y增大向上
            width = math.ceil((x_max - x_min) / d)
            height = math.ceil((y_max - y_min) / d)
            square = [[[] for j in range(0, height)] for i in range(0, width)]
            # 将牙齿表面数据点置入网格中
            for point in self.tooth.points[i]:
                x_index = math.floor((point[0] - x_min) / d)
                y_index = math.floor((point[1] - y_min) / d)
                square[x_index][y_index].append([point[0], point[1]])
            # 取每一列最外围两个网格，组成路径 （一头一尾，构成封闭路径）
            for m in range(0, len(square)):
                point_down = []
                point_up = []
                for n in range(0, len(square[m])):
                    # 单元格内存在点时，取均值
                    if len(square[m][n]) > 0:
                        x_sum = y_sum = 0
                        for point in square[m][n]:
                            x_sum = x_sum + point[0]
                            y_sum = y_sum + point[1]
                        point_down = [x_sum / len(square[m][n]), y_sum / len(square[m][n])]    
                        break
                for n in range(len(square[m]) - 1, -1, -1):
                    if len(square[m][n]) > 0:
                        x_sum = y_sum = 0
                        for point in square[m][n]:
                            x_sum = x_sum + point[0]
                            y_sum = y_sum + point[1]
                        point_up = [x_sum / len(square[m][n]), y_sum / len(square[m][n])]    
                        break
                if len(point_down) > 0:
                    self.boundary[i].insert(0, point_up)
                    self.boundary[i].append(point_down)

            # 判别每个网格周围四个网格是否都有点，如果有则说明该网格范围是牙齿的范围，钻头经过其中心即可覆盖该网格区域
            for m in range(1, len(square) - 1):
                for n in range(1, len(square[m]) - 1):
                    if (len(square[m][n]) > 0 and len(square[m-1][n]) > 0
                    and len(square[m+1][n]) > 0 and len(square[m][n-1]) > 0 and len(square[m][n+1]) > 0):
                        routine[i].append([x_min + m*d + 0.5*d, y_min + n*d + 0.5*d])
        return routine

    def getLength(self):
        return super().getLength()

    def visualizePoints(self):
        super().visualizePoints()
    
    def visualizeRoutine(self):
        # 设置刻度间隔
        x_major_locator=MultipleLocator(1)
        y_major_locator=MultipleLocator(1)
        for i in range(0, np.shape(self.routine)[0]):
            X = []
            Y = []
            for j in range(0, len(self.routine[i])):
                X.append(self.routine[i][j][0])
                Y.append(self.routine[i][j][1])
            plt.scatter(X, Y, color = "green", s = 50)
            X = []
            Y = []
            for j in range(0, len(self.tooth.points[i])):
                X.append(self.tooth.points[i][j][0])
                Y.append(self.tooth.points[i][j][1])
            plt.scatter(X, Y, color='red', s = 10)
            for j in range(0, len(self.boundary[i])):
                if j != 0:
                    plt.plot([self.boundary[i][j-1][0], self.boundary[i][j][0]], [self.boundary[i][j-1][1], self.boundary[i][j][1]], color = 'lightblue', linewidth = 1)
            if len(self.boundary[i]) > 1:        
                plt.plot([self.boundary[i][0][0], self.boundary[i][len(self.boundary[i])-1][0]], [self.boundary[i][0][1], self.boundary[i][len(self.boundary[i])-1][1]], color = 'lightblue', linewidth = 1)
            for j in range(0, len(self.routine[i])):
                if j != 0:
                    plt.plot([self.routine[i][j-1][0], self.routine[i][j][0]], [self.routine[i][j-1][1], self.routine[i][j][1]], color = 'green', linewidth = 1)
            ax = plt.gca()
            ax.xaxis.set_major_locator(x_major_locator)
            ax.yaxis.set_major_locator(y_major_locator)
            plt.grid()
            plt.show()

with open('route.pkl','rb') as f:
    points_data = pickle.load(f)
t = tooths(points_data)

routine1 = BasicRoutine(t)
print("BasicRoutine length: %f" % routine1.length)
routine2 = CoverageRoutine(t)
print("CoverageRoutine length: %f" % routine2.length)
routine2.visualizeRoutine()
