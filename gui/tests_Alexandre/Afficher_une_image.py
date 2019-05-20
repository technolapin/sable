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
        
        self.setMinimumSize(QSize(500, 500));
        
        self.setTabShape(1)
        self.onglet2 = QWidget()
        self.onglet3 = QWidget()  
        
        self.addTab( self.onglet2, "Aide" )
        self.addTab( self.onglet3, "Affichage de l'image" )
        
        self.image_1 = "Result1.pgm"             

        self.tabOnglet3()
        
        
        
    """
    Onglet 3
    """
    def tabOnglet3(self) :
        grille = QGridLayout()
        
        self.onglet3.setLayout(grille)
        self.label = QLabel() #self.centralwidget) 
        self.label.setPixmap(QPixmap(self.image_1))        
        grille.addWidget(self.label)
        
        

    def update_label(self, idx): 
       self.label.setScaledContents(not self.label.hasScaledContents()) 



if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = Fenetre() # Crée un objet de type Fenetre
    fenetre.setWindowTitle("Graphique 3D (DEMONSTRATION)") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    sys.exit(application.exec_()) # application.exec_() attend que tout ce qui est en cours soit exécuté





























































