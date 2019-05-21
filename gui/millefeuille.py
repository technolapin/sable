import os


from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png

import re

import numpy

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
import numpy as np



def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))


"""
img = read_pgm("test-0.pgm", byteorder='<')/255.
imagequimarche= plt.imread('JPEG_example_flower.jpg')/255.

image = img.astype(np.float64)



#x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
x, y = numpy.meshgrid(numpy.linspace(0,1,80), numpy.linspace(0,1,80))
ax = gca(projection='3d')
ax.plot_surface(x, y, numpy.array([0, 0]), rstride=5, cstride=5, facecolors=imagequimarche)
show()
"""


"""

imgALaCon = read_pgm("test-0.pgm", byteorder='<')

plt.matshow(imgALaCon)
"""
fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

'''
fn = get_sample_data("C:\Users\Amaury\Desktop\Sable\gui\JPEG_example_flower.png", asfileobj=False)
img = read_png(fn)

x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]]

ax = plt.gca(projection='3d')
ax.plot_surface(x, y, np.sin(0.02*x)*np.sin(0.02*y), rstride=2, cstride=2, facecolors=img)
plt.show()
'''

plt.show()