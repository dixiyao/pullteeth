import numpy as np
import matplotlib.pyplot as plt
import RayInsect
import boundary

# 多边形周长
# shape of polygon: [N, 2]
def Perimeter(polygon: np.array):
    N, d = polygon.shape
    if N < 3 or d != 2:
        raise ValueError

    permeter = 0.
    for i in range(N):
        permeter += np.linalg.norm(polygon[i-1] - polygon[i])
    return permeter


# 面积
def Area(polygon: np.array):
    N, d = polygon.shape
    if N < 3 or d != 2:
        raise ValueError

    area = 0.
    vector_1 = polygon[1] - polygon[0]
    for i in range(2, N):
        vector_2 = polygon[i] - polygon[0]
        area += np.abs(np.cross(vector_1, vector_2))
        vector_1 = vector_2
    return area / 2

# |r| < 1
# r > 0, 内缩
# r < 0, 外扩
def calc_shrink_width(polygon: np.array, r):
    area = Area(polygon)
    perimeter = Perimeter(polygon)
    L = area * (1 - r ** 2) / perimeter
    return L if r > 0 else -L


def shrink_polygon(polygon: np.array, r):
    N, d = polygon.shape
    if N < 3 or d != 2:
        raise ValueError

    shrinked_polygon = []
    L = r#calc_shrink_width(polygon, r)
    cov=RayInsect.Conv(polygon)
    print(len(cov))
    for i in range(N):
        if cov[i]==True:
            L=r
        else:
            L=-r
        Pi = polygon[i]
        v1 = polygon[i-1] - Pi
        v2 = polygon[(i+1)%N] - Pi

        normalize_v1 = v1 / np.linalg.norm(v1)
        normalize_v2 = v2 / np.linalg.norm(v2)

        sin_theta = np.abs(np.cross(normalize_v1, normalize_v2))

        Qi = Pi + L / sin_theta * (normalize_v1 + normalize_v2)

        if(RayInsect.isPoiWithinPoly(Qi,[polygon])):
            shrinked_polygon.append(Qi)
    return np.asarray(shrinked_polygon)

if __name__ == "__main__":
    #poly = np.array([[0.10207336523125997, 0.08024691358024691], [0.15151515151515152, 0.053497942386831275], [0.2025518341307815, 0.05555555555555555], [0.25199362041467305, 0.026748971193415638], [0.3157894736842105, 0.07407407407407407], [0.34290271132376393, 0.03909465020576132], [0.3923444976076555, 0.01646090534979424], [0.43381180223285487, 0.047325102880658436], [0.46730462519936206, 0.10493827160493827], [0.5151515151515151, 0.10493827160493827], [0.5741626794258373, 0.13580246913580246], [0.6028708133971292, 0.20987654320987653], [0.6060606060606061, 0.2777777777777778], [0.6698564593301436, 0.25308641975308643], [0.7240829346092504, 0.24897119341563786], [0.7799043062200957, 0.2613168724279835], [0.8437001594896332, 0.29835390946502055], [0.9043062200956937, 0.3662551440329218], [0.9569377990430622, 0.4732510288065844], [0.9585326953748007, 0.6358024691358025], [0.9202551834130781, 0.7551440329218106], [0.8835725677830941, 0.8106995884773662], [0.8309409888357256, 0.8600823045267489], [0.7751196172248804, 0.8888888888888888], [0.7097288676236044, 0.9032921810699589], [0.6076555023923444, 0.9794238683127572], [0.580542264752791, 0.9650205761316872], [0.44178628389154706, 0.9423868312757202], [0.430622009569378, 0.9218106995884774], [0.17543859649122806, 0.7078189300411523], [0.17384370015948963, 0.6851851851851852], [0.02711323763955343, 0.36213991769547327], [0.012759170653907496, 0.27983539094650206], [0.03827751196172249, 0.22839506172839505], [0.08452950558213716, 0.1831275720164609], [0.0861244019138756, 0.13168724279835392]])
    org,poly=boundary.get_estimated_boundary('test.png')
    poly=np.array(poly)
    org=np.array(org)
    perimeter = Perimeter(poly)
    area = Area(poly)

    shrink_poly = shrink_polygon(poly, 0.03)
    print(shrink_poly)

    for i in range(org.shape[0]):
        plt.plot([org[i-1][0],org[i][0]],[org[i-1][1],org[i][1]],color='green')
    for i in range(poly.shape[0]):
        plt.plot([poly[i-1][0],poly[i][0]],[poly[i-1][1],poly[i][1]],color='red')
    for i in range(shrink_poly.shape[0]):
        plt.plot([shrink_poly[i-1][0],shrink_poly[i][0]],[shrink_poly[i-1][1],shrink_poly[i][1]],color='blue')


    plt.show()
        
