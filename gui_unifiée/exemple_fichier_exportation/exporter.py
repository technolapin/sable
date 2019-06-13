# Source : https://www.geeksforgeeks.org/understanding-python-pickling-example/
import pickle # Permet de sauvegarder et charger des variables
# On n'utilise plus shelve, car il n'est pas cross-platform

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
ELLE DOIT ETRE RELATIVE AU FICHIER EXPORTE !
"""
URL_PGM = "../../extraction/coupes_3D/"

"""
URL du répertoire contenant les fichiers VTK
ELLE DOIT ETRE RELATIVE AU FICHIER EXPORTE !
"""
URL_VTK = "../../extraction/vtks/"

"""
Données du graphique à afficher
C'est une liste de listes de listes
Chaque sous-liste représente une courbe, et toutes ces sous-listes doivent avoir la même longueur
Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
Ces données doivent être exportées dans un fichier .npy via Numpy
ELLE DOIT ETRE RELATIVE AU FICHIER EXPORTE !
"""
URL_GRAPHIQUE_3D = "../../extraction/tracking_3D/resultats.npy"


"""
EXPORTATION
"""
# Bade de Données
bdd = {} 
bdd["NB_IMGS"] = NB_IMGS
bdd["INTERVALLE_XY"] = INTERVALLE_XY
bdd["INTERVALLE_XZ"] = INTERVALLE_XZ
bdd["INTERVALLE_YZ"] = INTERVALLE_YZ
bdd["URL_PGM"] = URL_PGM
bdd["URL_VTK"] = URL_VTK
bdd["URL_GRAPHIQUE_3D" ] = URL_GRAPHIQUE_3D

# Its important to use binary mode
fichierBdd = open('exemple', 'ab')

# source, destination
pickle.dump(bdd, fichierBdd)                 
fichierBdd.close()