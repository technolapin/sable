import os


from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
fn = get_sample_data(os.path.dirname(os.path.abspath(__file__)) + "/JPEG_example_flower.jpg", asfileobj=False)
img = read_png(fn)
x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
ax = gca(projection='3d')
ax.plot_surface(x, y, 10, rstride=5, cstride=5, facecolors=img)
show()