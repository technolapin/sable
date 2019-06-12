import os


"""
PARAMETRES
"""

PREFIX_VAR_ENV = "GUI_" # Peut être n'importe quoi
ANTI_LAG = True # Désactive l'affichache multi-couches dans le mille-feuilles
DISABLE_VTK = True # Désactiver l'onglet du VTK

try :
    NB_IMGS = int( os.environ[ PREFIX_VAR_ENV + "NB_IMGS" ] )
except KeyError :
    NB_IMGS = 4000 # Nombre d'images au format PGM

try :
    INTERVALLE_XY = int( os.environ[ PREFIX_VAR_ENV + "INTERVALLE_XY" ] )
except KeyError  :
    INTERVALLE_XY = 250 # Intervalle temporel dans cette liste d'images

try :
    URL_PGM = os.environ[ PREFIX_VAR_ENV + "URL_PGM" ]
except KeyError  :
    URL_PGM = "../extraction/coupes_3D/"

try :
    INTERVALLE_XZ = int( os.environ[ PREFIX_VAR_ENV + "INTERVALLE_XZ" ] )
except KeyError  :
    INTERVALLE_XZ = 80

try :
    INTERVALLE_YZ = int( os.environ[ PREFIX_VAR_ENV + "INTERVALLE_YZ" ] )
except KeyError  :
    INTERVALLE_YZ = 80

try :
    URL_VTK = "../extraction/vtks/"
except KeyError  :
    URL_VTK = 80


"""
VERIFICATION
"""
if NB_IMGS % INTERVALLE_XY != 0 :
    print( "On a un problème !" )
    sys.exit(1)