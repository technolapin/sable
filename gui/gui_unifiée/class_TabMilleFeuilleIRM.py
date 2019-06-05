import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_MilleFeuilleIRM import MilleFeuilleIRM

from parametres import *


"""
Classe TabMilleFeuilleIRM, hérite de la classe QGridLayout, c'est donc une grille
Cette classe représente le contenu d'une fenêtre PyQt
Elle peut donc aussi être utilisée comme un onglet dans une fenêtre
@author Amaury
"""
class TabMilleFeuilleIRM(QGridLayout) :
    """
    Constructeur, crée le contenu de l'onglet
    """
    def __init__(self, parent=None) :
        super(TabMilleFeuilleIRM, self).__init__(parent) # Appel du constructeur de QGridLayout
        
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
        
        # Ajout des Widgets
        self.addWidget( self.milleFeuilleIRM, 2, 1 )
        self.addWidget( self.barreDeScrollIRMCoucheX, 2, 2 )
        self.addWidget( self.barreDeScrollIRMCoucheY, 2, 3 )
        self.addWidget( self.barreDeScrollIRMCoucheZ, 2, 4 )
        self.addWidget( self.barreDeScrollIRMTemps, 3, 1 )
        
        self.dessinerMilleFeuilleIRM(0)
    
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
        
        print( "[Debug TabMilleFeuilleIRM] X : " + str( self.barreDeScrollIRMCoucheX.value() ) + ", Y : " + str( self.barreDeScrollIRMCoucheY.value() ) + ", Z : " + str( self.barreDeScrollIRMCoucheZ.value() ) + ", Temps : " + str( self.barreDeScrollIRMTemps.value() ) )
        print( "[Debug TabMilleFeuilleIRM] Affichage : " + imageX + ", " + imageY + ", " + imageZ )


"""
Code principal pour démonstration
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = QWidget() # Crée un objet de type QWidget
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.setLayout( TabMilleFeuilleIRM() )
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté