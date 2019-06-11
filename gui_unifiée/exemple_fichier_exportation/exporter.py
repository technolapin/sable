# Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=sauve_recup_objets
import shelve # Permet de sauvegarder et charger des variables

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
Ces données doivent être exportées dans un fichier .npy via Numpy
"""
URL_GRAPHIQUE_3D = "../extraction/tracking_3D/resultats.npy"


"""
EXPORTATION
"""
fichierExportation = shelve.open( 'exemple' )

fichierExportation["NB_IMGS"] = NB_IMGS
fichierExportation["INTERVALLE_XY"] = INTERVALLE_XY
fichierExportation["INTERVALLE_XZ"] = INTERVALLE_XZ
fichierExportation["INTERVALLE_YZ"] = INTERVALLE_YZ
fichierExportation["URL_PGM"] = URL_PGM
fichierExportation["URL_VTK"] = URL_VTK
fichierExportation["URL_GRAPHIQUE_3D" ] = URL_GRAPHIQUE_3D

fichierExportation.close()