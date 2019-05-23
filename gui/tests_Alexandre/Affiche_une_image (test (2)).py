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
        self.image_1 = "Test1.pgm" 
        self.image_2 = "Image_btn_g"	
        self.image_3 = "Image_btn_d"
        self.centralwidget    = QWidget(Viewer) 
        self.gridLayout       = QGridLayout(self.centralwidget) 
        self.verticalLayout_2 = QVBoxLayout() 
        self.horizontalLayout = QHBoxLayout() 


        
        # QLabel 
        self.label = QLabel(self.centralwidget) 
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, 
                                		QSizePolicy.Fixed) 
        self.label.setSizePolicy(sizePolicy) 
        self.label.setPixmap(QPixmap(self.image_1)) 
        self.label.setScaledContents(False) 
        self.horizontalLayout.addWidget(self.label)         
        
        self.verticalLayout = QVBoxLayout() 
        spacerItem = QSpacerItem(20, 18, QSizePolicy.Minimum, 
        	                        	QSizePolicy.Fixed) 
        self.verticalLayout.addItem(spacerItem) 
        self.horizontalLayout.addLayout(self.verticalLayout) 
        self.verticalLayout_2.addLayout(self.horizontalLayout) 
        self.horizontalLayout_2 = QHBoxLayout()         


        
        # QPushButton 
        self.pushButton1 = QPushButton(self.centralwidget) 
        self.pushButton1.setText("Image précédente") 
        
        self.pushButton2 = QPushButton(self.centralwidget) 
        self.pushButton2.setText("Image suivante") 
        
        icon1 = QIcon() 
        icon1.addPixmap(QPixmap(self.image_2),QIcon.Normal, 
                                        QIcon.Off)
        icon2 = QIcon() 
        icon2.addPixmap(QPixmap(self.image_3),QIcon.Normal, 
                                        QIcon.Off)
        
        self.pushButton1.setIcon(icon1) 
        self.horizontalLayout_2.addWidget(self.pushButton1) 
        
        self.pushButton2.setIcon(icon2) 
        self.horizontalLayout_2.addWidget(self.pushButton2) 
        

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)         
        
        
        
        self.horizontalLayout_3 = QHBoxLayout() 
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, 
                                    	QSizePolicy.Minimum) 
        self.horizontalLayout_3.addItem(spacerItem1) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        
        
        self.horizontalLayout_4 = QHBoxLayout() 
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, 
                                    	QSizePolicy.Minimum) 
        self.horizontalLayout_4.addItem(spacerItem2) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        
        
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1) 
        Viewer.setCentralWidget(self.centralwidget) 
        

        
    def update_push_button1(self, idx): 
        if not idx: 
            return 
        if idx == 1:
            self.pushButton1.setAutoDefault(not self.pushButton1.autoDefault()) 
        elif idx == 2: 
            self.pushButton1.setDefault(not self.pushButton1.isDefault()) 
        else: 
            self.pushButton1.setFlat(not self.pushButton1.isFlat()) 
        
        
        
    def update_push_button2(self, idx): 
        if not idx: 
            return 
        if idx == 1:
            self.pushButton2.setAutoDefault(not self.pushButton2.autoDefault()) 
        elif idx == 2: 
            self.pushButton2.setDefault(not self.pushButton2.isDefault()) 
        else: 
            self.pushButton2.setFlat(not self.pushButton2.isFlat()) 
        
        
        
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