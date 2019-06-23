import sys

"""
PARAMETRES PAR DEFAUT
Utilisées uniquement par la classe Parametres dans class_Parametres.py
Ecrasés si chargement d'un fichier d'importation
"""
NB_IMGS = 4000 # Nombre d'images au format PGM
INTERVALLE_XY = 250 # Intervalle temporel dans cette liste d'images
URL_PGM = "../extraction/coupes_3D/"
INTERVALLE_XZ = 80
INTERVALLE_YZ = 80
URL_VTK = "../extraction/vtk_3D/"
URL_GRAPHIQUE_3D = "../extraction/tracking_3D/resultats.npy"
URL_VITESSE_MOY_GRAINS = "../extraction/tracking_3D/vitesse_moy_grains.npy"

"""
VERIFICATION
"""
if NB_IMGS % INTERVALLE_XY != 0 :
    print( "[Erreur Paramètres] On a un problème !" )
    sys.exit(1)