# pullteeth
## 切除程序
通过计算机和UR5机械手进行交互，按照给定的路径规划将牙齿切除。
### 主要程序介绍
1. Step1: ```registration_data_gather.py```: Connect UR5 (自动完成)。医生在头模模型上采集点，采集50个点。每次采集完成后，电脑反馈提示音，并采集下一个点。生成采集到的点保存在```data.pkl```中
2. Step2: ```registration.py```: ICP registration：通过ICP算法，进行配准，需要stl格式的头模模型，需要拔除的牙齿模型，将机器人，牙齿，头部，和计算机图像四者进行一体配准。生成路径。此程序中路径生成算法较为简单，合适的路径规划算法请参考section 路径规划部分程序，并复写此程序中的```getremovepoints_index```和```getremovepoints_byindex```函数。在机器人坐标下，待切除的位置点在```route.pkl```中。
3. Step3. ```control1.py```: 连接机械臂(UR5)。按照Step2中规划好的路径，指挥机械手移动。请修改第18行```delegate.connect(('169.254.1.3',30002))```中的ip地址和端口号以便正确连接。由于现在系统还是alpha版本，所以中断点比较多，在初始开启，以及等待医生开启钻头，到达初始点位，每切除一层都会暂停，键盘输入任意键即可继续。
### 对于树脂块单牙根牙实验
* icp.py 用来生成单牙的路径，也可以拟合单牙和颌骨模型。
* control1.py 用生成的单牙路径进行磨削切除
### 对于静态模型试验
* registration_data_gather.py 通过用机器人在模型上划动找到配准点
* registration.py 继承icp中的类，配准颌骨模型到机器人坐标，同时配准牙齿到颌骨，统一头骨CT图像坐标和机器人坐标，生成路径
### 其他文件
* realtime.py 用于3D可视化路径
* accuracy.py 用于拟合计算牙齿切除效果
* boundary.py 计算2维图像边界
* polyshrink.py用于收缩二维模型边界
### 依赖
``` 
pickle, sklearn, numpy, vtk, open3d
```
### 联系方式
github: dixiyao  
mail: dixi.yao@mail.utoronto.ca

## 路径规划
```route_planning.py```中完成路径规划的任务，```registration.py```中生成的```route.pkl```作为输入， 规划的路径坐标在Routine类中的routine中存储，visualizePoints和visualizeRoutine中有可视化结果。

现有程序中包含两个路径规划算法：

1. BasicRoutine是将所有数据点按顺序连起来的路径，由于数据点的特性（可实验分析），路径非常长，不适合使用。仅作为Baseline。

2. CoverageRoutine是通过网格覆盖法获取的路径。基本思路是，由于磨削工具本身具有一定的大小（1mm直径），其经过之处可以覆盖一定的牙齿区域。因此可以将整个三维牙齿模型视为若干二维平面，磨削这些平面并不断深入磨削工具即可完成磨削。而磨削一个平面又可以看成是覆盖这个平面所有的区域，因此我们只需要寻找哪些点需要被覆盖，再将它们相连即可得到路径。

   具体方法为：

   1. 以z轴将三维模型划分成若干牙齿平面(registration.py中已完成)
   2. 对每个平面划分成若干d*d矩形网格(square), 以灰色可视化
   3. 将散点置入网格中, 以红色可视化
   4. 取每一列最外的两个点连成路径, 构成外围轮廓(self.boundary), 以浅蓝色可视化
   5. 判定哪些网格中心需要被覆盖(由于磨削工具本身具有直径, 经过网格中心即说明网格区域被覆盖), 以绿色可视化
   6. 将这些网格中心按顺序连接即得到路径routine, 以绿色可视化

   说明：

   1. 网格大小等于磨削工具的直径; 可以修改, 但需要考虑刀具能覆盖多少网格的问题

   2. 刀具的覆盖范围是一个圆, 需要考虑网格的四个角

   3. 算法还有很多需要完善的地方：

      - 数据点分布在外围，内部部分网格没有数据点，用“周围四个网格有数据点”判定网格需要覆盖会导致缺失。所以后面几个结果图的路径会缺失          

        可能的解决方案: 从每个网格中心出发, 沿x和y正负方向作射线, 与第四步求得的boundary相交. x和y正负方向分别有且仅有一个交点则说明在内部, 根据距离判断路径是否应经过

      - boundary出现凹陷(图上表现为尖角), 同样是因为数据点分散的问题. 可以考虑删除斜率过大的点对应的线段, 因为通常情况下牙齿截面应该是相对较为规则的多边形

      - 路径直接将需要覆盖的网格点相连. 不是最短距离, 可以优化, 但差距不大.

### 联系方式
github: qbl0
mail: andrew_yan@sjtu.edu.cn