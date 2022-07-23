import util
import numpy as np
import open3d as o3d

densifyN = 20000

def den(s_file):
    shape_file=s_file+'.obj'
    V, E, F = util.parseObj(shape_file)
    F = util.removeWeirdDuplicate(F)
    Vorig, Eorig, Forig = V.copy(), E.copy(), F.copy()

    # sort by length (maintain a priority queue)
    Elist = list(range(len(E)))
    Elist.sort(key=lambda i: util.edgeLength(V, E, i), reverse=True)

    # create edge-to-triangle and triangle-to-edge lists
    EtoF = [[] for j in range(len(E))]
    FtoE = [[] for j in range(len(F))]
    for f in range(len(F)):
        v = F[f]
        util.pushEtoFandFtoE(EtoF, FtoE, E, f, v[0], v[1])
        util.pushEtoFandFtoE(EtoF, FtoE, E, f, v[0], v[2])
        util.pushEtoFandFtoE(EtoF, FtoE, E, f, v[1], v[2])
    V, E, F = list(V), list(E), list(F)

    # repeat densification
    for z in range(densifyN):
        util.densify(V, E, F, EtoF, FtoE, Elist)

    densifyV = np.array(V[-densifyN:])

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(densifyV)

    o3d.io.write_point_cloud(s_file+'.ply', pcd)
    #o3d.visualization.draw_geometries([pcd])

den('2')