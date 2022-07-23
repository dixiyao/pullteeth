import numpy as np
import open3d as o3d
import pymesh
import stl
import math


def distance(i,j):
    return math.sqrt((i[0]-j[0])*(i[0]-j[0])+(i[1]-j[1])*(i[1]-j[1])+(i[2]-j[2])*(i[2]-j[2]))

class original_and_then():
    def __init__(self,orgname,cutname):
        #dense.den(orgname)
        #dense.den(cutname)
        org = o3d.geometry.PointCloud(o3d.io.read_triangle_mesh(orgname+'.stl').vertices)
        new = o3d.geometry.PointCloud(o3d.io.read_triangle_mesh(cutname+'.stl').vertices)

        # 为两个点云上上不同的颜色
        org.paint_uniform_color([1, 0.706, 0])  # source 为黄色
        new.paint_uniform_color([0, 0.651, 0.929])  # target 为蓝色

        threshold = 100.0  # 移动范围的阀值
        trans_init = np.asarray([[1, 0, 0, 0],  # 4x4 identity matrix，这是一个转换矩阵，
                                    [0, 1, 0, 0],  # 象征着没有任何位移，没有任何旋转，我们输入
                                    [0, 0, 1, 0],  # 这个矩阵为初始变换
                                    [0, 0, 0, 1]])

        # 运行icp
        reg_p2p = o3d.pipelines.registration.registration_icp(
                org,new, threshold, trans_init,
                o3d.pipelines.registration.TransformationEstimationPointToPoint())

        org.transform(reg_p2p.transformation)

        self.org = org
        self.new = new

        self.orgname = orgname
        self.newname = cutname

        self.org.estimate_normals()
        self.new.estimate_normals()
        self.orgmesh=o3d.io.read_triangle_mesh(self.orgname+'.stl')
        self.orgmesh.vertices=self.org.points
        self.newmesh = o3d.io.read_triangle_mesh(self.newname + '.stl')
        self.newmesh.vertices = self.new.points
        self.orgmesh.compute_triangle_normals()
        self.orgmesh.compute_vertex_normals()
        self.newmesh.compute_triangle_normals()
        self.newmesh.compute_vertex_normals()
        o3d.io.write_triangle_mesh(self.orgname + '_cal.stl',self.orgmesh)
        o3d.io.write_triangle_mesh(self.newname + '_cal.stl',self.newmesh)

    def visualize(self):
        o3d.visualization.draw_geometries([self.org,self.new])

    def volume_calculation(self):
        orgmesh=stl.Mesh.from_file(self.orgname+'.stl')
        newmesh = stl.Mesh.from_file(self.newname + '.stl')
        self.orgvolume, cog, inertia = newmesh.get_mass_properties()
        self.newvolume, cog, inertia = orgmesh.get_mass_properties()
        print('original volume: ',self.orgvolume,self.newvolume)
        orgmesh = stl.Mesh.from_file(self.orgname + '_cal.stl')
        newmesh = stl.Mesh.from_file(self.newname + '_cal.stl')
        self.orgvolume, cog, inertia = newmesh.get_mass_properties()
        self.newvolume, cog, inertia = orgmesh.get_mass_properties()
        print('reconstruction volume: ',self.orgvolume, self.newvolume)

    def intersection(self):
        orgmesh = pymesh.load_mesh(self.orgname + '_cal.stl')
        newmesh = pymesh.load_mesh(self.newname + '_cal.stl')
        intersection = pymesh.boolean(orgmesh, newmesh, "intersection")
        print(intersection.attribute_names)
        pymesh.save_mesh("intersection.stl", intersection)
        intersection=stl.mesh.Mesh.from_file('intersection.stl')
        volume,_,_=intersection.get_mass_properties()
        print('intersection volume: ', volume)

if __name__=='__main__':
    pair = original_and_then('36','48')
    pair.volume_calculation()
    pair.intersection()