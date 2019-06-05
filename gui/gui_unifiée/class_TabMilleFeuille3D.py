import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_MilleFeuille3D import MilleFeuille3D

from parametres import *


"""
Classe TabGraphique3D, hérite de la classe QWidget uniquement pour pouvoir l'exécuter indépendemment
Cette classe permet de gérer la fenêtre Qt, mais elle peut aussi être utilisée comme un onglet dans une autre fenêtre
@author Amaury
"""
class TabMilleFeuille3D(QWidget) :
    """
    Constructeur, crée le contenu de l'onglet
    """
    def __init__(self, parent=None) :
        if __name__ == '__main__' :
            super(TabMilleFeuille3D, self).__init__(parent) # Appel du constructeur de QWidget, uniquement pour pouvoir l'exécuter indépendemment
        
        # Graphe à afficher
        self.milleFeuille3D = MilleFeuille3D()
        
        # Défilement de couches inférieures (Valeur de la couche minimum à afficher)
        self.barreDeScrollMFCoucheMin = QScrollBar()
        self.barreDeScrollMFCoucheMin.setMaximum( INTERVALLE_XY - 1 )
        self.barreDeScrollMFCoucheMin.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        # Défilement de couches supérieures (Valeur de la couche maximum à afficher)
        self.barreDeScrollMFCoucheMax = QScrollBar()
        self.barreDeScrollMFCoucheMax.setMaximum( INTERVALLE_XY - 1 )
        self.barreDeScrollMFCoucheMax.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        # Défilement temporel
        self.barreDeScrollMFTemps = QScrollBar(Qt.Horizontal)
        self.barreDeScrollMFTemps.setMaximum( NB_IMGS / INTERVALLE_XY - 1 )
        self.barreDeScrollMFTemps.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        self.grille = QGridLayout()
        
        self.grille.addWidget( self.milleFeuille3D, 2, 1 )
        self.grille.addWidget( self.barreDeScrollMFCoucheMin, 2, 2 )
        if not ANTI_LAG : grille.addWidget( self.barreDeScrollMFCoucheMax, 2, 3 )
        # Ne pas l'afficher quand l'ANTI_LAG est activé, donc inutilisable, donc une seule couche affichée
        self.grille.addWidget( self.barreDeScrollMFTemps, 3, 1 )
        
        self.dessinerMilleFeuille3D(0)
        
        if __name__ == '__main__' :
            self.setLayout(self.grille) # Definit notre grille comme grille à utiliser, uniquement pour pouvoir l'exécuter indépendemment
    
    """
    Accesseur à la grille de l'onglet
    @return La grille de l'onglet, c'est à dire sont contenu
    Cette grille est utilisable par : onglet.setLayout( grille )
    """
    def getGrille(self) :
        return self.grille
    
    """
    Gère le dessin et les changements du mille-feuilles 3D
    """
    def dessinerMilleFeuille3D(self, value) :
        # Si ANTI_LAG est activé, ET/OU que barreDeScrollMFCoucheMax est à 0 (Forcément si ANTI_LAG), on ne commande qu'avec barreDeScrollMFCoucheMin
        listeImages = [] # Liste des images que on veut afficher dans le mille-feuilles
        if self.barreDeScrollMFCoucheMax.value() != 0 : # Commander le défilement avec les deux barres
            for i in range(self.barreDeScrollMFCoucheMin.value(), self.barreDeScrollMFCoucheMax.value(), 1) :
                urlImage = URL_POUR_MF + str(self.barreDeScrollMFTemps.value() * INTERVALLE_X + i) + ".pgm" # Chemin de l'image
                hauteurImage = self.barreDeScrollMFCoucheMin.value() + i # Hauteur de l'image dans le mille-feuille
                listeImages.append( [urlImage, hauteurImage] )
        else : # Permet de ne commander qu'avec le défilement de la valeur minimum, forcément si ANTI_LAG activé
            numeroImage = self.barreDeScrollMFTemps.value() * INTERVALLE_XY + self.barreDeScrollMFCoucheMin.value()
            listeImages.append( [URL_POUR_MF + str(numeroImage) + ".pgm", self.barreDeScrollMFCoucheMin.value()] )
        
        self.milleFeuille3D.dessinerMilleFeuille3D( listeImages )
        
        print( "[Debug MF] Min : " + str( self.barreDeScrollMFCoucheMin.value() ) + ", Max : " + str( self.barreDeScrollMFCoucheMax.value() ) + ", Temps : " + str( self.barreDeScrollMFTemps.value() ) )
        if ANTI_LAG : print( "[Debug MF] Affichage : " + URL_POUR_MF + str(numeroImage) + ".pgm" )


"""
Code principal pour démonstration
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = TabMilleFeuille3D() # Crée un objet de type TabMilleFeuille3D
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté
