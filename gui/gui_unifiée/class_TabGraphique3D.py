import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_Graphique3D import Graphique3D

from parametres_pour_demo import grapheDeDemonstration


"""
Classe TabGraphique3D, hérite de la classe QWidget uniquement pour pouvoir l'exécuter indépendemment
Cette classe permet de gérer la fenêtre Qt, mais elle peut aussi être utilisée comme un onglet dans une autre fenêtre
@author Amaury
"""
class TabGraphique3D(QWidget) :
    """
    Constructeur, crée le contenu de l'onglet
    """
    def __init__(self, grapheDonne, parent=None) :
        if __name__ == '__main__' :
            super(TabGraphique3D, self).__init__(parent) # Appel du constructeur de QWidget, uniquement pour pouvoir l'exécuter indépendemment
        
        # Graphe à afficher
        self.graphe = grapheDonne
        
#        self.menuSelection = QComboBox() # C'est un menu déroulant
#        self.menuSelection.addItems(['Graph1', 'Graph2']) # Ajoute les indexes de ce menu
#        self.menuSelection.currentIndexChanged.connect(self.changementGraphique3D) # La procédure à appeler lors du changement
        
        self.graphique3D = Graphique3D()
#        self.graphique3D.setMinimumSize(QSize(400, 400)) # Définit la taille minimum en pixels de ce Widget
#        # Cela permet de bloquer le trop retrécissement de la fenêtre
#        # On peut remplacer "QSize(400, 400)" par "self.graphique3D.sizeHint()" pour que la taille par défaut soit la taille minimum
#       Devenu inutile car on définit la taille minimale de la fenêtre
        
        # Défilement coupes
        self.barreDeScrollCourbes = QScrollBar() # C'est une barre de défilement
        self.barreDeScrollCourbes.setMaximum( len(self.graphe[0]) ) # Défini le nombre de valeurs qu'on peut y parcourir
        # len(self.graphe[0][0]) est le nombre de courbes
        self.barreDeScrollCourbes.valueChanged.connect( self.dessinerGraphique3D ) # La procédure à appeler lorsque l'utilisateur y touche
        
        # Défilement temporel
        self.barreDeScrollTemps = QScrollBar()
        self.barreDeScrollTemps.setMaximum( len(self.graphe[0][0]) )
        # len(self.graphe[0][0]) est le nombre d'échantillons temporels dont on dispose
        self.barreDeScrollTemps.valueChanged.connect( self.dessinerGraphique3D )
        
        self.grille = QGridLayout() # C'est l'intérieur de la fenêtre, une grille ("layout")
        
#        self.grille.addWidget( self.menuSelection, 1, 1 ) # Ajoute le menu déroulant en position ligne 2 colonne 1
        self.grille.addWidget( self.graphique3D, 2, 1 ) # Ajoute le graphique 3D en position ligne 2 colonne 1
        self.grille.addWidget( self.barreDeScrollCourbes, 2, 2 ) # Ajoute la barre de défilement 1 en position ligne 2 colonne 2
        self.grille.addWidget( self.barreDeScrollTemps, 2, 3 ) # Ajoute la barre de défilement 2 en position ligne 2 colonne 2
            
        self.dessinerGraphique3D(0) # Afficher graphique de base
        
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
    Gère le dessin et les changements par l'utilisateur dans les barres de défilement
    """
    def dessinerGraphique3D(self, value) :
#        graphiqueDemande = str(self.menuSelection.currentText())
#        if graphiqueDemande == "Graph1" :
#            self.graph1()
#        if graphiqueDemande == "Graph2" :
#            self.graph2()
#       Devenu inutlie puisqu'on a supprimé les menus déroulants
         self.graphique3D.dessinerGraphique3D( self.graphe, self.barreDeScrollCourbes.value(), self.barreDeScrollTemps.value() )
         
         print( "[Debug 3D] Temps : " + str( self.barreDeScrollCourbes.value() ) + ", Courbe : " + str( self.barreDeScrollTemps.value() ) + ", Valeur donnée : " + str( value ) )


"""
Code principal pour démonstration
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = TabGraphique3D( grapheDeDemonstration ) # Crée un objet de type TabMilleFeuille3D
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté
