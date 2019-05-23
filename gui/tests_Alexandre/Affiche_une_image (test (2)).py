"""
Created on Fri May 17 11:09:54 2019

@author: leblona
"""

# -*- coding: utf-8 -*- 

import sys 
import os 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
        
class ImageViewer(object): 
    def setupUi(self, Viewer): 
        Viewer.resize(640, 480) 
        Viewer.setWindowTitle(u"Test de création de boutons") 	
        self.image_1 = "wesh.pgm"       # Image "principale"
        self.image_2 = "Image_btn_g"	# Icone du bouton de gauche
        self.image_3 = "Image_btn_d"     # Icone du couton de droite
        self.centralwidget    = QWidget(Viewer) 
        self.gridLayout       = QGridLayout(self.centralwidget) 
        self.verticalLayout_2 = QVBoxLayout() 
        self.horizontalLayout = QHBoxLayout() 


        
        # QLabel 
        self.label = QLabel(self.centralwidget) 
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed) 
        self.label.setSizePolicy(sizePolicy) 
        self.label.setPixmap(QPixmap(self.image_1)) 
        self.label.setScaledContents(False) 
        self.horizontalLayout.addWidget(self.label)         
        
        self.verticalLayout = QVBoxLayout() 
        spacerItem = QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Fixed) 
        self.verticalLayout.addItem(spacerItem) 
        self.horizontalLayout.addLayout(self.verticalLayout) 
        self.verticalLayout_2.addLayout(self.horizontalLayout) 
        self.horizontalLayout_2 = QHBoxLayout()         


        
        # QPushButton 
        
        # Bouton 1
        self.pushButton1 = QPushButton(self.centralwidget) 
        self.pushButton1.setText("Image précédente") 
       
        icon1 = QIcon() 
        icon1.addPixmap(QPixmap(self.image_2),QIcon.Normal, QIcon.Off)
        
        self.pushButton1.setIcon(icon1) 
        
        # Bouton 2    
    
        self.pushButton2 = QPushButton(self.centralwidget) 
        self.pushButton2.setText("Image suivante") 
        
        icon2 = QIcon() 
        icon2.addPixmap(QPixmap(self.image_3),QIcon.Normal, QIcon.Off)
        
        self.pushButton2.setIcon(icon2) 

        # Ajout des boutons au Layout

        self.horizontalLayout_2.addWidget(self.pushButton1) 
        self.horizontalLayout_2.addWidget(self.pushButton2) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)                 
        
        # Positionnement des boutons grâce à des QSpacerItem
        
        self.horizontalLayout_3 = QHBoxLayout() 
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.horizontalLayout_3.addItem(spacerItem1) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        
        
        self.horizontalLayout_4 = QHBoxLayout() 
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.horizontalLayout_4.addItem(spacerItem2) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        
        
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1) 
        Viewer.setCentralWidget(self.centralwidget) 
        
        
        
    def je_sers_a_rien_mais_ca_fonctionne_pas_sans_moi(self, idx): 
        return 
        
        
        
        grille = QGridLayout()
        
        self.Viewer.setLayout(grille)
        self.label = QLabel() #self.centralwidget) 
        self.label.setPixmap(QPixmap(self.image_1))
        grille.addWidget(self.label)
        
        

if __name__ == "__main__": 
    import sys 
    app = QApplication(sys.argv) 
    Viewer = QMainWindow() 
    ui = ImageViewer() 
    ui.setupUi(Viewer) 
    Viewer.show() 	
    sys.exit(app.exec_()) 