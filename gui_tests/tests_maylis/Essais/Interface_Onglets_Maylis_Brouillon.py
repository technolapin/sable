# -*- coding: utf-8 -*-
"""
Environnement graphique d'affichage de graphiques en 3D
Utilise la librairie PyQt pour l'UI, et MatPlotLib pour les graphiques

"""

import sys # Librairie pour faire des appels systèmes
from PyQt4.QtCore import * # Librairie Python Qt4 pour créer la GUI
from PyQt4.QtGui import *

from math import * 
import numpy

from matplotlib.figure import Figure # Librairie Matplotlib pour les graphiques
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg 
from mpl_toolkits.mplot3d import Axes3D # Classe pour gérer les axes 3D

from random import choice


"""
Classe Graphique3D, hérite de FigureCanvasQTAgg
Cette classe permet de gérer un graphique 3D Matplotlib pouvant être tourné et inséré dans un environnement Qt
"""
class Graphique3D(FigureCanvasQTAgg) :

    """
    Constructeur, initialise le graphique
    """
    def __init__(self) :
        # Création d'un Canvas allant contenir le graphique 3D
        self.figure = plt.figure(figsize=(7,7))
        FigureCanvasQTAgg.__init__(self, self.figure) 
        self.axes = self.figure.gca(projection='3d') 
        
    """
    Dessine ou actualise avec un nouveau graphique
    Le paramètre "liste" est une liste de listes
    Chaque sous-liste représente une courbe
    Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
    """
    def dessinerGraphique3D(self, liste) : 
        # Initialisation des paramètres du graphique 3D
        self.axes.clear() 
        self.axes.set_xlabel('Axe X') 
        self.axes.set_ylabel('Axe Y') 
        self.axes.set_zlabel('Axe Z')
        self.axes.set_aspect('equal')
        for courbe in liste :
            couleur = choice(["b", "g", "r", "c", "m", "y"]) 
            self.axes.plot(courbe[0], courbe[1], courbe[2], couleur + 'o-') 
        self.draw()


"""
Classe Fenetre, hérite de la classe QWidget
Cette classe permet de gérer la fenêtre Qt
Le graphique 3D est inséré dedans
"""
class Fenetre(QTabWidget):

    """
    Constructeur
    """
    def __init__(self, parent = None):
        # Initialisation de la fenêtre
        super(Fenetre, self).__init__(parent)
        # Création des onglets de la fenêtre
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()  
        # Ajout des onglets à la fenêtre  	    
        self.addTab(self.tab1,"Tab 1") 
        self.addTab(self.tab2,"Tab 2")
        self.addTab(self.tab3,"Tab 3")
        # Association aux contenus des onglets
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("Analyse de mouvements de grains de sable dans une sequence d'images 3D")
		
    """
    Génère le contenu de l'onglet 1
    """       
    def tab1UI(self):
        # Création de la grille dans laquelle on va placer les objets
        layout = QGridLayout()
        # Création du Graphique 3D
        graphique3D = Graphique3D()
        graphique3D.setMinimumSize(QSize(400, 400))        
        # Création des barres de défilement et ajout des options
        self.barreDeScroll1 = QScrollBar()
        self.barreDeScroll1.setMaximum( len(graphe[0][0]) )
        self.barreDeScroll1.sliderMoved.connect(self.changementGraphique3D)
        self.barreDeScroll2 = QScrollBar()
        self.barreDeScroll2.setMaximum(255)
        self.barreDeScroll2.sliderMoved.connect(self.changementGraphique3D)
        # Ajout des éléments dans la grille
        layout.addWidget(graphique3D,2,1)
        layout.addWidget(self.barreDeScroll1,2,2)
        layout.addWidget(self.barreDeScroll2,2,3)
        
        self.setTabText(0,"Visualisation graphique") # Ajout d'un titre à l'onglet
        self.tab1.setLayout(layout) # Ajout du contenu dans l'onglet 1
        graphique3D.dessinerGraphique3D(graphe) 


    """
    Gère les changements par l'utilisateur dans le menu déroulant de sélection
    """
    def changementGraphique3D(self) :
#        graphiqueDemande = str(self.menuSelection.currentText())
#        if graphiqueDemande == "Graph1" :
#            self.graph1()
#        if graphiqueDemande == "Graph2" :
#            self.graph2()
         self.barreDeScroll1.value()



    """
    Génère le contenu de l'onglet 2 ## A CHANGER
    """       
    def tab2UI(self):
        # Création d'un questionnaire
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"),sex)
        layout.addRow("Date of Birth",QLineEdit())
        self.setTabText(1,"Personal Details")
        self.tab2.setLayout(layout)
	
    """
    Génère le contenu de l'onglet 3 ## A CHANGER
    """       
    def tab3UI(self):
        # Création d'une box
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects")) 
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(2,"Education Details")
        self.tab3.setLayout(layout)
	

	
"""
Code principal
"""      

# Fonctions à représenter
theta = numpy.linspace(-10 * numpy.pi, 5 * numpy.pi, 100)
z = numpy.linspace(-2, 2, 100)
r = z**2 + 1
x = r * numpy.sin(theta)
y = r * numpy.cos(theta)

courbe1 = [x, y, z]
courbe2 = [y, z, x]
courbe3 = [z, x, y]

# Note : Notre programme n'utilise que cette variable globale "graphe"
graphe = [courbe1, courbe2, courbe3]

        
def main():
     application = QApplication(sys.argv)
     interface = Fenetre()
     interface.show()
     sys.exit(application.exec_())
	
if __name__ == '__main__':
     main()