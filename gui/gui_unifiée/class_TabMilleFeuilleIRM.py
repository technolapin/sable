import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_MilleFeuilleIRM import MilleFeuilleIRM

from parametres import *


"""
Classe TabGraphique3D, hérite de la classe QWidget uniquement pour pouvoir l'exécuter indépendemment
Cette classe permet de gérer la fenêtre Qt, mais elle peut aussi être utilisée comme un onglet dans une autre fenêtre
@author Amaury
"""
class TabMilleFeuilleIRM(QWidget) :
    """
    Constructeur, crée le contenu de l'onglet
    """
    def __init__(self, parent=None) :
        if __name__ == '__main__' :
            super(TabMilleFeuilleIRM, self).__init__(parent) # Appel du constructeur de QWidget, uniquement pour pouvoir l'exécuter indépendemment
        
        # Graphe à afficher
        self.milleFeuilleIRM = MilleFeuilleIRM()
        
        # Défilement de la couche X
        self.barreDeScrollIRMCoucheX = QScrollBar()
        self.barreDeScrollIRMCoucheX.setMaximum( INTERVALLE_YZ - 1 )
        self.barreDeScrollIRMCoucheX.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        # Défilement de la couche Y
        self.barreDeScrollIRMCoucheY = QScrollBar()
        self.barreDeScrollIRMCoucheY.setMaximum( INTERVALLE_XZ - 1 )
        self.barreDeScrollIRMCoucheY.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        # Défilement de la couche Z
        self.barreDeScrollIRMCoucheZ = QScrollBar()
        self.barreDeScrollIRMCoucheZ.setMaximum( INTERVALLE_XY - 1 )
        self.barreDeScrollIRMCoucheZ.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        # Défilement temporel
        self.barreDeScrollIRMTemps = QScrollBar(Qt.Horizontal)
        self.barreDeScrollIRMTemps.setMaximum( NB_IMGS / INTERVALLE_XY - 1 )
        self.barreDeScrollIRMTemps.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        self.grille = QGridLayout()
        
        self.grille.addWidget( self.milleFeuilleIRM, 2, 1 )
        self.grille.addWidget( self.barreDeScrollIRMCoucheX, 2, 2 )
        self.grille.addWidget( self.barreDeScrollIRMCoucheY, 2, 3 )
        self.grille.addWidget( self.barreDeScrollIRMCoucheZ, 2, 4 )
        self.grille.addWidget( self.barreDeScrollIRMTemps, 3, 1 )
        
        self.dessinerMilleFeuilleIRM(0)
        
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
    Gère le dessin et les changements de l'affichage IRM
    """
    def dessinerMilleFeuilleIRM(self, value) :
        coucheXFormate = format(self.barreDeScrollIRMCoucheX.value(), '04d') # String sur 4 digits
        coucheYFormate = format(self.barreDeScrollIRMCoucheY.value(), '04d') # String sur 4 digits
        coucheZFormate = format(self.barreDeScrollIRMCoucheZ.value(), '04d') # String sur 4 digits
        tempsFormate = format(self.barreDeScrollIRMTemps.value(), '02d') # String sur 2 digits
        
        imageX = URL_POUR_IRM + "y_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_yz_" + coucheXFormate + ".pgm"
        imageY = URL_POUR_IRM + "x_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_xz_" + coucheYFormate + ".pgm"
        imageZ = URL_POUR_IRM + "x_y/" + tempsFormate + "/t_" + tempsFormate + "coupe_xy_" + coucheZFormate + ".pgm"
        
        self.milleFeuilleIRM.dessinerMilleFeuilleIRM( [imageX, self.barreDeScrollIRMCoucheX.value() ],
                                                      [imageY, self.barreDeScrollIRMCoucheY.value() ], 
                                                      [imageZ, self.barreDeScrollIRMCoucheZ.value() ] )
        
        print( "[Debug IRM] X : " + str( self.barreDeScrollIRMCoucheX.value() ) + ", Y : " + str( self.barreDeScrollIRMCoucheY.value() ) + ", Z : " + str( self.barreDeScrollIRMCoucheZ.value() ) + ", Temps : " + str( self.barreDeScrollIRMTemps.value() ) )
        print( "[Debug IRM] Affichage : " + imageX + ", " + imageY + ", " + imageZ )


"""
Code principal pour démonstration
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = TabMilleFeuilleIRM() # Crée un objet de type TabMilleFeuilleIRM
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté
