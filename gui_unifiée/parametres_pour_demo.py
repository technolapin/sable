from numpy import linspace, pi, sin, cos, load

"""
PARAMETRES
Graphique pour démonstration
"""
# Graphique que on veut afficher
theta = linspace(-10 * pi, 5 * pi, 100)
z = linspace(-2, 2, 100)
r = z**2 + 1
x = r * sin(theta)
y = r * cos(theta)

resultats = load("../extraction/tracking_3D/resultats.npy")

#courbe1 = [x, y, z]
#courbe2 = [y, z, x]
#courbe3 = [z, x, y]
courbe1 = resultats[0]
courbe2 = resultats[1]
courbe3 = resultats[2]
# Note : Notre programme n'utilise que cette variable globale "graphe"
#grapheDeDemonstration = [courbe1, courbe2, courbe3]
grapheDeDemonstration = resultats[30:50]
# Elle doit être une liste de listes
# Chaque sous-liste représente une courbe, et toutes ces sous-listes doivent avoir la même longueur
# Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
