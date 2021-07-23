from mpl_toolkits import mplot3d
#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from read_data import tooth
import vtk
from vtk.util.numpy_support import numpy_to_vtk

def data_actor(source_data):
    # 新建 vtkPoints 实例
    points = vtk.vtkPoints()
    # 导入点数据
    points.SetData(numpy_to_vtk(source_data))
    # 新建 vtkPolyData 实例
    polydata = vtk.vtkPolyData()
    # 设置点坐标
    polydata.SetPoints(points)

    # 顶点相关的 filter
    vertex = vtk.vtkVertexGlyphFilter()
    vertex.SetInputData(polydata)

    # mapper 实例
    mapper = vtk.vtkPolyDataMapper()
    # 关联 filter 输出
    mapper.SetInputConnection(vertex.GetOutputPort())

    # actor 实例
    actor = vtk.vtkActor()
    # 关联 mapper
    actor.SetMapper(mapper)
    return actor


def data_actor_stl(filename):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
 
    mapper = vtk.vtkPolyDataMapper()

    mapper.SetInputConnection(reader.GetOutputPort())
 
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor
    

def show_actor(actor_list):
    # render
    render = vtk.vtkRenderer()
    render.SetBackground(0, 0, 0)

    # Renderer Window
    window = vtk.vtkRenderWindow()
    window.AddRenderer(render)
    window.SetSize(1200, 1200)

    # System Event
    win_render = vtk.vtkRenderWindowInteractor()
    win_render.SetRenderWindow(window)

    # Style
    win_render.SetInteractorStyle(vtk.vtkInteractorStyleMultiTouchCamera())

    # Insert Actor
    for actor in actor_list:
        render.AddActor(actor)
    win_render.Initialize()
    win_render.Start()

t=tooth(r'T T_Green_Split_002.stl')
t.transform_reverse_up_and_down()
points=t.points
data=[]
red=[]

for j in range(t.levels):
    for i in range(0,len(t.points[j])): 
        data.append(points[j][i])
        if j==0 and i in [0]:#,1,2]:
          red.append(points[j][i])  
data=np.array(data)
red=np.array(red)
'''
#ac1=data_actor_stl(r'T T_Green_Split_002.stl')
ac1=data_actor(data)
ac2=data_actor(red)
ac2.GetProperty().SetColor(1,0,0)
ac2.GetProperty().SetPointSize(10)
show_actor([ac1,ac2])
'''
x=[]
y=[]
z=[]
for k in range(3,4):
    for i in range(len(t.points[k])):
        x.append(t.points[k][i][0])
        y.append(t.points[k][i][1])
        z.append(t.points[k][i][2])
plt.plot(np.array(x),np.array(y))
plt.show()

