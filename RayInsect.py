'''
判断点是否在图形内，点是否是凹点
'''
import numpy as np
def isRayIntersectsSegment(poi,s_poi,e_poi): #[x,y] [lng,lat]
    #输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    if s_poi[1]==e_poi[1]: #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]: #线段在射线上边
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]: #线段在射线下边
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]: #交点为下端点，对应spoint
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]: #交点为下端点，对应epoint
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]: #线段在射线左边
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1]) #求交
    if xseg<poi[0]: #交点在射线起点的左侧
        return False
    return True  #排除上述情况之后

def isPoiWithinPoly(poi,poly):
    #输入：点，多边形三维数组
    #poly=[[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]],[[w1,t1],……[wk,tk]]] 三维数组

    #可以先判断点是否在外包矩形内 
    #if not isPoiWithinBox(poi,mbr=[[0,0],[180,90]]): return False
    #但算最小外包矩形本身需要循环边，会造成开销，本处略去
    sinsc=0 #交点个数
    for epoly in poly: #循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
        for i in range(len(epoly)-1): #[0,len-1]
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            if isRayIntersectsSegment(poi,s_poi,e_poi):
                sinsc+=1 #有交点就加1

    return True if sinsc%2==1 else  False


def find_ymax(data):
    """寻找封闭图形中y坐标最大的点
       若y坐标最大点不止一个，则寻找其中x坐标最大点
    Args:
        data (list): 封闭图形点集
    Returns:
        封闭图形中第一个凸点
    """
    ploy = np.array(data)
    y = ploy[:,1]
    y_max = y.max()
    Conv_list = list()
    for p in data:
        if p[1] == y_max:
            Conv_list.append(p)
    
    if len(Conv_list) != 1:
        temp_list = []
        for p in Conv_list:
            temp_list.append(p[0])
        return Conv_list[temp_list.index(max(temp_list))]
    else:
        return Conv_list[0]
    
def Conv(data):
    data=data.tolist()
    """对多边形各点进行凹凸性判断
    Args:
        data (list): 封闭图形点集
    Returns:
        [list]: 多边形中凹点坐标集合
    """
    Norm_dot = find_ymax(data)
    num = len(data)
    Ind = data.index(Norm_dot)
    Conv_dots = []
    Vec_A = [data[Ind%num][0] - data[(Ind-1)%num][0], data[Ind%num][1] - data[(Ind-1)%num][1]]
    Vec_B = [data[(Ind+1)%num][0] - data[Ind%num][0], data[(Ind+1)%num][1] - data[Ind%num][1]]
    Vect_Norm = (Vec_A[0] * Vec_B[1]) - (Vec_A[1] * Vec_B[0])
    # 向量法判断图形中每个点的凹凸性
    for i in range(num):
        V_A = [data[(i)%num][0] - data[(i-1)%num][0], data[(i)%num][1] - data[(i-1)%num][1]]
        V_B = [data[(i+1)%num][0] - data[(i)%num][0], data[(i+1)%num][1] - data[(i)%num][1]]
        Vec_Cross = (V_A[0] * V_B[1]) - (V_A[1] * V_B[0])
        Conv_dots.append(Vec_Cross * Vect_Norm>0)
    
    return Conv_dots
