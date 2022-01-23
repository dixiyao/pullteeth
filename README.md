# pullteeth
## 现在用到的文件
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