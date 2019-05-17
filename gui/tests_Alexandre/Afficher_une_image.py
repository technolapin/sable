#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:27:45 2019

@author: leblona
"""
import sys 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 



class Fenetre(QTabWidget) :
    """
    Constructeur
    """
    def __init__(self, parent=None) :
        super(Fenetre, self).__init__(parent) # Appel du constructeur de QWidget
        
        # Impose la taille minimale de la fenêtre, en pixels
        self.setMinimumSize(QSize(500, 500));
        
        # Création des onglets de la fenêtre
        self.setTabShape(1)
        self.onglet1 = QWidget()
        self.onglet2 = QWidget()
        self.onglet3 = QWidget()  
        self.centralwidget = QWidget() 
        
        # Ajout des onglets à la fenêtre  	    
        self.addTab( self.onglet1, "Visualisation du Graphique" ) 
        self.addTab( self.onglet2, "Aide" )
        self.addTab( self.onglet3, "Affichage de l'image" )
        
        # On choisit l'image à afficher dans l'onglet 3
        self.image_1 = "Result1.pgm"             

        # Appel des procédures qui remplissent les onglets        
        self.tabOnglet3()
        
        
        
    """
    Onglet 3
    """
    def tabOnglet3(self) :
        grille = QGridLayout()
        
        self.onglet3.setLayout(grille)
        #Affichage de l'image        
        self.label = QLabel(self.centralwidget) 
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed) 
        self.label.setSizePolicy(sizePolicy) 
        self.label.setPixmap(QPixmap(self.image_1))        
        self.label.setScaledContents(False)
        self.label.adjustSize()
        self.label_cmb = QComboBox(self.centralwidget)
        self.label_cmb.currentIndexChanged.connect(self.update_label) 
        grille.addWidget(self.label)
        
        

    def update_label(self, idx): 
       self.label.setScaledContents(not self.label.hasScaledContents()) 



if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = Fenetre() # Crée un objet de type Fenetre
    fenetre.setWindowTitle("Graphique 3D (DEMONSTRATION)") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    sys.exit(application.exec_()) # application.exec_() attend que tout ce qui est en cours soit exécuté





























































