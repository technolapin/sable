import parametres


"""
Objet de centralisation des paramètres
"""
class Parametres() :
    def __init__(self) :
        """
        Valeurs par défaut
        """
        self.contientDesVariablesImportees = False
        
        self.NB_IMGS = parametres.NB_IMGS # Nombre d'images au format PGM
        self.INTERVALLE_XY = parametres.INTERVALLE_XY # Intervalle temporel dans cette liste d'images, c'est à dire le pas dans le plan XY
        self.INTERVALLE_XZ = parametres.INTERVALLE_XZ # Pas dans le plan XZ
        self.INTERVALLE_YZ = parametres.INTERVALLE_YZ # Pas dans le plan YZ
        self.URL_PGM = parametres.URL_PGM # URL vers les fichiers PGM
        self.URL_VTK = parametres.URL_VTK # URL vers les fichiers VTK
        self.URL_GRAPHIQUE_3D = parametres.URL_GRAPHIQUE_3D # URL vers le fichier NPY
        self.CHEMIN_ABSOLU_FICHIER_IMPORTE = None # Chemin absolu du fichier contenant les params importés
        
        self.TabGraphique3D = None # Objet TabGraphique3D
    
    def setNB_IMGS( self, param ) :
        self.NB_IMGS = param
        self.contientDesVariablesImportees = True
    def setINTERVALLE_XY( self, param ) :
        self.INTERVALLE_XY = param
        self.contientDesVariablesImportees = True
    def setINTERVALLE_XZ( self, param ) :
        self.INTERVALLE_XZ = param
        self.contientDesVariablesImportees = True
    def setINTERVALLE_YZ( self, param ) :
        self.INTERVALLE_YZ = param
        self.contientDesVariablesImportees = True
    def setURL_PGM( self, param ) :
        self.URL_PGM = param
        self.contientDesVariablesImportees = True
    def setURL_VTK( self, param ) :
        self.URL_VTK = param
        self.contientDesVariablesImportees = True
    def setURL_GRAPHIQUE_3D( self, param ) :
        self.URL_GRAPHIQUE_3D = param
        self.contientDesVariablesImportees = True
    def setCHEMIN_ABSOLU_FICHIER_IMPORTE( self, param ) :
        self.CHEMIN_ABSOLU_FICHIER_IMPORTE = param
        self.contientDesVariablesImportees = True
    
    def setTabGraphique3D( self, param ) :
        self.TabGraphique3D = param
    def getTabGraphique3D(self):
        return self.TabGraphique3D
    
    def contientDesVariablesImportees(self) :
        return self.contientDesVariablesImportees
    
    """
    @return True si il y a une logique, False sinon
    """
    def verifierParams(self) :
        if self.NB_IMGS % self.INTERVALLE_XY != 0 :
                return False
        return True
    
    
    """
    @param plan : Le plan de la caméra, 'YZ', 'XZ' ou 'XY'
    @param instantTemporel : L'instant temporel du PGM
    @param couche : Le numéro de la couche du PGM
    """
    def genererURLdesPGM3D( self, plan, instantTemporel, couche ) :
        coucheFormate = format(couche, '04d') # String sur 4 digits
        tempsFormate = format(instantTemporel, '02d') # String sur 2 digits
        
        if plan == 'YZ' :
            fichierPGM = self.URL_PGM + "y_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_yz_" + coucheFormate + ".pgm"
        if plan == 'XZ' :
            fichierPGM = self.URL_PGM + "x_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_xz_" + coucheFormate + ".pgm"
        if plan == 'XY' :
            fichierPGM = self.URL_PGM + "x_y/" + tempsFormate + "/t_" + tempsFormate + "coupe_xy_" + coucheFormate + ".pgm"
        return fichierPGM
    
    """
    @param instantTemporel : L'instant temporel du VTK
    """
    def genererURLdesVTK( self, instantTemporel ) :
        tempsFormate = format(instantTemporel, '02d') # String sur 2 digits
        fichierVTK = self.URL_VTK + tempsFormate + ".vtk"
        return fichierVTK
    
    """
    @return URL du fichier NPY à utiliser
    """
    def genererURLGraph3D(self) :
        return self.URL_GRAPHIQUE_3D
    
    
    """
    @return Nombre d'images dans le plan de la caméra YZ, moins 1
    """
    def nombreImagesPlanYZ(self) :
        return self.INTERVALLE_YZ - 1
    
    """
    @return Nombre d'images dans le plan de la caméra YZ, moins 1
    """
    def nombreImagesPlanXZ(self) :
        return self.INTERVALLE_XZ - 1
    
    """
    @return Nombre d'images dans le plan de la caméra YZ, moins 1
    """
    def nombreImagesPlanXY(self) :
        return self.INTERVALLE_XY - 1
    
    """
    @return Nombre d'instants temporels, moins 1
    """
    def nombreInstantsTemporels(self) :
        return self.NB_IMGS / self.INTERVALLE_XY - 1