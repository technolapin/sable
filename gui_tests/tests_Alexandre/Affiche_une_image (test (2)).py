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
        self.image_1 = "rangee/00/tranche-0000t00.pgm"       # Image "principale"
        self.image_2 = "Image_btn_g"	                    # Icone du bouton de gauche
        self.image_3 = "Image_btn_d"                         # Icone du couton de droite
        self.centralwidget    = QWidget(Viewer) 
        self.gridLayout       = QGridLayout(self.centralwidget) 
        self.verticalLayout   = QVBoxLayout() 
        self.horizontalLayout = QHBoxLayout() 


        
        # QLabel 
        self.label = QLabel(self.centralwidget) 
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed) 
        self.label.setSizePolicy(sizePolicy) 
        self.label.setPixmap(QPixmap(self.image_1)) 
        self.label.setScaledContents(False) 
        self.horizontalLayout.addWidget(self.label)        
        
        self.verticalLayout.addLayout(self.horizontalLayout) 
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
        self.verticalLayout.addLayout(self.horizontalLayout_2)                 
        
        
        
        # Positionnement des boutons grâce à un QSpacerItem
        
        self.horizontalLayout_3 = QHBoxLayout() 
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum) 
        self.horizontalLayout_3.addItem(spacerItem2) 
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        
        
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1) 
        Viewer.setCentralWidget(self.centralwidget) 
        

        

if __name__ == "__main__": 
    import sys 
    app = QApplication(sys.argv) 
    Viewer = QMainWindow() 
    ui = ImageViewer() 
    ui.setupUi(Viewer) 
    Viewer.show() 	
    sys.exit(app.exec_()) 