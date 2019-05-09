# Source : https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#line-plots


import numpy as np



theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)


"""
Pour chaque grains de sable :
x = [ x, x, x, x ]
y = [ y, y, y, y ]
z = [ z, z, z, z ]
      =========> t
Chaque indice des listes est un instant t
"""

"""
GENERATION D'UNE COURBE EN 3D
"""
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15,15))
ax = fig.gca(projection='3d')
# b = blue
# o = mettre des ronds
# - = lier ces ronds
ax.plot(x, y, z, 'bo-', label='Courbe 1')
ax.plot(z, x, y, 'ro-', label='Courbe 2')
ax.plot(y, z, x, 'go-', label='Courbe 3')
ax.legend()

plt.show()
