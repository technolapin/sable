"""
FICHIER D'EXPORTATION DU TRAITEMENT
Ce fichier contient les informations nécéssaires sur un traitement d'image déjà réalisé
Cela permet de charger les données sans re-faire le traitement
"""

"""
Nombre d'images total dans le fichier PGM
"""
NB_IMGS = 4000

"""
Intervalles temporelles dans le plan XY, c'est à dire dans le fichier précédent
"""
INTERVALLE_XY = 250

"""
Intervalles temporelles dans le plan XZ
"""
INTERVALLE_XZ = 80

"""
Intervalles temporelles dans le plan YZ
"""
INTERVALLE_YZ = 80

"""
URL du répertoire contenant les coupes 3D
"""
URL_PGM = "../extraction/coupes_3D/"

"""
URL du répertoire contenant les fichiers VTK
"""
URL_VTK = "../extraction/vtks/"

"""
Données du graphique à afficher
C'est une liste de listes de listes
Chaque sous-liste représente une courbe, et toutes ces sous-listes doivent avoir la même longueur
Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
"""
graphe = []