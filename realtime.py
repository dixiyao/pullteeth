import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from read_data import tooth

def Gen_RandLine(length, dims=2) :
    lineData = np.empty((dims, length))
    lineData[:, 0] = np.random.rand(dims)
    for index in range(1, length) :
        # scaling the random numbers by 0.1 so
        # movement is small compared to position.
        # subtraction by 0.5 is to change the range to [-0.5, 0.5]
        # to allow a line to move backwards.
        step = ((np.random.rand(dims) - 0.5) * 0.1)
        lineData[:, index] = lineData[:, index-1] + step

    return lineData

def update_lines(num, dataLines, lines,ct_levels) :
    for line, data in zip(lines, dataLines) :
        print(data)
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[:2, num-ct_levels[num]:num])
    return lines

t=tooth(r'T T_Green_Split_002.stl')
#t.transform_reverse_up_and_down()
#t.transform_z_negetive()
points=[]
ct_levels=[]
for i in range(0,len(t.points)):
    for j in range(len(t.points[i])):
        points.append(t.points[i][j])
        ct_levels.append(j)
# Attaching 3D axis to the figure
plt.axis('square')
fig ,ax=plt.subplots()


# Fifty lines of random 3-D lines
data=np.array(points).transpose()
ax.plot(data[0,:], data[1,:],alpha=0.5)
ax.axis('square')
lines = [ax.plot(data[0,:], data[1,:])[0]]
# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, data.shape[1], fargs=([data], lines,ct_levels),
                              interval=50, blit=False)

plt.show()
