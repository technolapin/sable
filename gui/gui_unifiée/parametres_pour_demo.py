import numpy

"""
PARAMETRES
Graphique pour démonstration
"""
# Graphique que on veut afficher
theta = numpy.linspace(-10 * numpy.pi, 5 * numpy.pi, 100)
z = numpy.linspace(-2, 2, 100)
r = z**2 + 1
x = r * numpy.sin(theta)
y = r * numpy.cos(theta)

courbe1 = [x, y, z]
courbe2 = [y, z, x]
courbe3 = [z, x, y]

# Note : Notre programme n'utilise que cette variable globale "graphe"
grapheDeDemonstration = [courbe1, courbe2, courbe3]
# Elle doit être une liste de listes
# Chaque sous-liste représente une courbe, et toutes ces sous-listes doivent avoir la même longueur
# Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer