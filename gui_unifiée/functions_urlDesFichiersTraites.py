from parametres import *

"""
@param plan : Le plan de la caméra, 'YZ', 'XZ' ou 'XY'
@param instantTemporel : L'instant temporel du PGM
@param couche : Le numéro de la couche du PGM
"""
def genererURLdesPGM3D( plan, instantTemporel, couche ) :
    coucheFormate = format(couche, '04d') # String sur 4 digits
    tempsFormate = format(instantTemporel, '02d') # String sur 2 digits
    
    if plan == 'YZ' :
        fichierPGM = URL_PGM + "y_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_yz_" + coucheFormate + ".pgm"
    if plan == 'XZ' :
        fichierPGM = URL_PGM + "x_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_xz_" + coucheFormate + ".pgm"
    if plan == 'XY' :
        fichierPGM = URL_PGM + "x_y/" + tempsFormate + "/t_" + tempsFormate + "coupe_xy_" + coucheFormate + ".pgm"
    return fichierPGM

"""
@param instantTemporel : L'instant temporel du VTK
"""
def genererURLdesVTK( instantTemporel ) :
    tempsFormate = format(instantTemporel, '02d') # String sur 2 digits
    fichierVTK = URL_VTK + tempsFormate + ".vtk"
    return fichierVTK

"""
@return URL du fichier NPY à utiliser
"""
def genererURLGraph3D() :
    return URL_GRAPHIQUE_3D


"""
@return Nombre d'images dans le plan de la caméra YZ, moins 1
"""
def nombreImagesPlanYZ() :
    return INTERVALLE_YZ - 1

"""
@return Nombre d'images dans le plan de la caméra YZ, moins 1
"""
def nombreImagesPlanXZ() :
    return INTERVALLE_XZ - 1

"""
@return Nombre d'images dans le plan de la caméra YZ, moins 1
"""
def nombreImagesPlanXY() :
    return INTERVALLE_XY - 1

"""
@return Nombre d'instants temporels, moins 1
"""
def nombreInstantsTemporels() :
    return NB_IMGS / INTERVALLE_XY - 1
