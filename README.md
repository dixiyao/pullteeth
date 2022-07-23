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
