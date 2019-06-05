"""
PARAMETRES
"""

ANTI_LAG = True # Désactive l'affichache multi-couches dans le mille-feuilles

NB_IMGS = 4000 # Nombre d'images au format PGM
INTERVALLE_XY = 250 # Intervalle temporel dans cette liste d'images
URL_POUR_MF = "../../extraction/images/test-"

URL_POUR_IRM = "../../extraction/coupes_3D/"
INTERVALLE_XZ = 80
INTERVALLE_YZ = 80

if NB_IMGS % INTERVALLE_XY != 0 :
    print( "On a un problème !" )
    sys.exit(1)
