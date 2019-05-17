# -*- coding: utf-8 -*-

import sys # Librairie pour faire des appels systèmes

from PyQt4.QtCore import * # Librairie Python Qt4 pour créer la GUI
from PyQt4.QtGui import *
import codecs
import io

class Fenetre(QTabWidget):
    def __init__(self, parent = None):
        super(Fenetre, self).__init__(parent)
        self.setMinimumSize( QSize(500, 500) );
        # Création des onglets de la fenêtre
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.setTabShape(1)
        self.addTab(self.tab1,"Tab 1")
        self.addTab(self.tab2,"Tab 2")
        self.tab1UI()
        self.tab2UI()
        self.setWindowTitle("Analyse de mouvements de grains de sable dans une sequence d'images 3D")
        
    def tab1UI(self):
        # Création de la grille dans laquelle on va placer les objets
        layout=QGridLayout()

        ### Contenu de la grille 
        
        # Création d'un objet contenant les différents onglets
        onglets = QTabWidget()
        # Création des onglets et ajout dans l'objet contenant les onglets        
        onglet1 = QWidget()
        onglet2 = QWidget()
        onglet3 = QWidget()
        onglets.addTab( onglet1, "Onglet 1" ) 
        onglets.addTab( onglet2, "Onglet 2" )
        onglets.addTab( onglet3, "Onglet 3" )
        onglets.setTabPosition(2)
        onglets.setTabShape(1)
        # Ajout des onglets dans la grille
        layout.addWidget(onglets)
        self.tab1.setLayout(layout)
        
        
        ### Contenu des onglets
        zone_de_texte = QHBoxLayout()
        scroll_area=QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        
        fichier=codecs.open("C:/Users/Maylis/Documents/1.COURS/4.ESIEE/PROJET/sable/gui/tests_maylis/Aide_generale.html", 'r',encoding='utf-8')
        texte=QLabel(fichier.read())
        texte.adjustSize()
        texte.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        texte.setWordWrap(True)
        texte.setAlignment(Qt.AlignJustify)
        scroll_area.setWidget(texte)
        zone_de_texte.addWidget(scroll_area)
        onglet1.setLayout(zone_de_texte)
        

    
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
	
        
        
def main():
     application = QApplication(sys.argv)
     interface = Fenetre()
     interface.show()
     sys.exit(application.exec_())
	
if __name__ == '__main__':
     main()
     
     
     
fichier = open("urlfichier")
list=fichier.readlines()
concatenation=""
for i in range (len(list)):
    concatenation+=list[i]