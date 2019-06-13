import os
import sys


"""
PARAMETRES
"""

PREFIX_VAR_ENV = "GUI_" # Peut être n'importe quoi
ENABLE_ANTI_LAG = True # Désactive l'affichache multi-couches dans le mille-feuilles

try :
    NB_IMGS = int( os.environ[ PREFIX_VAR_ENV + "NB_IMGS" ] )
    print("caca")
except KeyError :
    NB_IMGS = 4000 # Nombre d'images au format PGM

try :
    INTERVALLE_XY = int( os.environ[ PREFIX_VAR_ENV + "INTERVALLE_XY" ] )
    print("caca")
except KeyError  :
    INTERVALLE_XY = 250 # Intervalle temporel dans cette liste d'images

try :
    URL_PGM = os.environ[ PREFIX_VAR_ENV + "URL_PGM" ]
    print("caca")
except KeyError  :
    URL_PGM = "../extraction/coupes_3D/"

try :
    INTERVALLE_XZ = int( os.environ[ PREFIX_VAR_ENV + "INTERVALLE_XZ" ] )
    print("caca")
except KeyError  :
    INTERVALLE_XZ = 80

try :
    INTERVALLE_YZ = int( os.environ[ PREFIX_VAR_ENV + "INTERVALLE_YZ" ] )
    print("caca")
except KeyError  :
    INTERVALLE_YZ = 80

try :
    URL_VTK = os.environ[ PREFIX_VAR_ENV + "URL_VTK" ]
    print("caca")
except KeyError  :
    URL_VTK = "../extraction/vtks/"

try :
    URL_GRAPHIQUE_3D = os.environ[ PREFIX_VAR_ENV + "URL_GRAPHIQUE_3D" ]
    print("caca")
except KeyError  :
    URL_GRAPHIQUE_3D = "../extraction/tracking_3D/resultats.npy"


"""
VERIFICATION
"""
if NB_IMGS % INTERVALLE_XY != 0 :
    print( "[Paramètres] On a un problème !" )
    sys.exit(1)