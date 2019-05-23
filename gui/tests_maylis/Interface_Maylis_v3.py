# -*- coding: utf-8 -*-

"""
Environnement graphique d'affichage de graphiques en 3D
Utilise la librairie PyQt pour l'UI, et MatPlotLib pour les graphiques
Ce code est basé sur un code trouvé sur StackOverflow.com qui correspondait à ce que nous voulions faire
Source : https://stackoverflow.com/questions/52379426/pyqta-matplotlib-how-to-redraw-update-a-3d-surface-plot-in-a-window
Auteurs originaux :
- "Sreeletha" : https://stackoverflow.com/users/10374297/sreeletha
- "Joe" : https://stackoverflow.com/users/7919597/joe
"""


import sys 
from random import choice 
import codecs # Pour l'ouverture d'un fichier

# Librairie Python Qt4 pour créer la GUI
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

# Outils mathématiques
from math import *
import numpy 

# Outils de visualisation graphique
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg 
from mpl_toolkits.mplot3d import Axes3D 



"""
Classe Graphique3D, hérite de FigureCanvasQTAgg
Cette classe permet de gérer un graphique 3D Matplotlib pouvant être tourné et inséré dans un environnement Qt
"""
class Graphique3D(FigureCanvasQTAgg) :
    """
    Constructeur
    """
    def __init__(self) :
        self.figure = plt.figure()
        self.figure.subplots_adjust(bottom=0, top=1, left=0, right=1) # Supprime les marges
        FigureCanvasQTAgg.__init__( self, self.figure ) 
        self.axes = self.figure.gca( projection = '3d' ) # Axes 3D, et stockage dans un attribut
    
    """
    Dessine ou actualise avec un nouveau graphique
    Le paramètre "liste" est une liste de listes
    Chaque sous-liste représente une courbe
    Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
    @param "courbeAfficher" : La courbe à afficher dans "liste" + 1, 0 si il faut les afficher toutes
    @param "tempsAfficher" : L'instant à afficher dans "liste" + 1, 0 si il faut afficher tous les instants
    """
    def dessinerGraphique3D(self, liste, courbeAfficher, tempsAfficher) : 
        self.axes.clear() 
        self.axes.set_xlabel( 'Axe X' ) 
        self.axes.set_ylabel( 'Axe Y' )
        self.axes.set_zlabel( 'Axe Z' ) 
        #self.axes.set_aspect( 'equal' ) # Permet d'avoir un repère orthonormal
        if courbeAfficher != 0 :
            couleur = choice( ["b", "g", "r", "c", "m", "y"] ) # Choix aléatoire de couleurs de base de Matplotlib
            self.axes.plot( liste[courbeAfficher - 1][0], liste[courbeAfficher - 1][1], liste[courbeAfficher - 1][2], couleur + 'o-' ) 
        else :
            for courbe in liste :
                couleur = choice( ["b", "g", "r", "c", "m", "y"] ) # Choix aléatoire de couleurs de base de Matplotlib
                self.axes.plot( courbe[0], courbe[1], courbe[2], couleur + 'o-' )
        self.draw() 


"""
Classe Fenetre, hérite de la classe QTabWidget (Et plus QWidget vu qu'on veut faire des onglets)
Cette classe permet de gérer la fenêtre Qt avec onglets (Appel de la procédure "addTab()")
Le graphique 3D est inséré dedans
"""
class Fenetre(QTabWidget) :
    """
    Constructeur
    """
    def __init__(self, parent=None) :
        # Appel du constructeur de QWidget
        super(Fenetre, self).__init__(parent) 
        
        # Impose la taille minimale de la fenêtre, en pixels
        self.setMinimumSize( QSize(500, 500) );
        
        # Création des onglets de la fenêtre
        self.setTabShape(1)
        self.visu_graph = QWidget()
        self.aide = QWidget()
      #  self.selection_grain = QWidget()  
        self.affichage_image = QWidget()

        # Dictionnaire des onglets de la fenêtre 
        self.ongl_fen = { 'visu_graph' :        [self.visu_graph,         "Visualisation du Graphique", self.tabGraphique3D()       ] , 
                          'aide' :              [self.aide ,              "Aide",                       self.tabAide()              ] , 
                         # 'selection_grain' :   [self.selection_grain ,   "Selection du grain",         self.tabselection_grain()   ] , 
                          'affichage_image' :   [self.affichage_image,    "Affichage coupe 2D",         self.tabaffichage_image()   ]}
        
        # Ajout dynamique des onglets dans la fenêtre
        for ongl in self.ongl_fen :
            self.addTab(self.ongl_fen[ongl][0], self.ongl_fen[ongl][1]) # Ajout des onglets à la fenêtre
            self.ongl_fen[ongl][2] # Appel procédures remplissant les onglets
        
    

    """
    Onglet du graphique 3D
    """
    def tabGraphique3D(self) :
        self.graphique3D = Graphique3D()
        
        # Défilement temporel
        self.barreDeScrollCourbes = QScrollBar() 
        self.barreDeScrollCourbes.setMaximum( len(graphe[0]) + 1 ) # Défini le nombre de valeurs qu'on peut y parcourir

        self.barreDeScrollCourbes.valueChanged.connect( self.changementGraphique3D ) # Procédure à appeler lorsque l'utilisateur y touche
        
        # Défilement coupes
        self.barreDeScrollTemps = QScrollBar()
        self.barreDeScrollTemps.setMaximum( len(graphe[0][0]) + 1 )
        self.barreDeScrollTemps.valueChanged.connect( self.changementGraphique3D )
        
        # Organisation deu graphique et des barres de défilement dans la fenêtre
        grille = QGridLayout() 
        grille.addWidget( self.graphique3D, 2, 1 ) 
        grille.addWidget( self.barreDeScrollCourbes, 2, 2 )
        grille.addWidget( self.barreDeScrollTemps, 2, 3 )
        self.setLayout(grille) 
        
        self.graphique3D.dessinerGraphique3D( graphe, 0, 0 ) # Afficher graphique de base
        
        self.visu_graph.setLayout(grille) # Ajout du contenu dans l'onglet


    """
    Gère les changements par l'utilisateur dans le menu déroulant de sélection
    """
    def changementGraphique3D(self, value) :
         self.graphique3D.dessinerGraphique3D( graphe, self.barreDeScrollCourbes.value(), self.barreDeScrollTemps.value() )
        # print( "[Debug] Temps : " + str( self.barreDeScrollCourbes.value() ) + ", Courbe : " + str( self.barreDeScrollTemps.value() ) + ", Valeur donnée : " + str( value ) )


    
    
    
    """
    Onglet 2
    """
    def tabAide(self) :
        # Création d'un layout
        layout=QGridLayout()

        # Création d'onglets dans la page d'aide
        onglets = QTabWidget()
        onglets.setTabPosition(2)
        onglets.setTabShape(1)

        aide_ongl = QWidget()
        aide_onglet1 = QWidget()
        aide_onglet2 = QWidget()
    
        # Dictionnaire des onglets de la page d'aide
        self.ongl_aide = { 'aide_ongl' :   [aide_ongl,     "Introduction", 'Aide_generale.html'] , 
                          'aide_onglet1' : [aide_onglet1 , "Aide Onglet1", 'coucou.html'       ] , 
                          'aide_onglet2' : [aide_onglet2 , "Aide_Onglet2", 'salut.html'        ] }
        
        # Ajout dynamique des onglets à la page d'aide
        for ongl in self.ongl_aide :
            onglets.addTab(self.ongl_aide[ongl][0], self.ongl_aide[ongl][1])
            self.contenu_onglet_aide(ongl)
        
        # Ajout du conteneur d'onglets dans la grille et du layout dans l'onglet Aide de la fenêtre
        layout.addWidget(onglets)
        self.aide.setLayout(layout)
        
    
    """
    Affiche dans l'onglet indiqué le contenu du fichier .html associé
    """    
    def contenu_onglet_aide(self, nom_onglet)       :  
        # Contenant avec barre de scroll
        zone_de_texte = QHBoxLayout()
        scroll_area=QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        
        # Ouverture du fichier contenant l'aide écrite au format .html  
        lien_fichier='contenu_aide/'+self.ongl_aide[nom_onglet][2]
        fichier=codecs.open(lien_fichier, 'r',encoding='utf-8')
        texte=QLabel(fichier.read())
        
        # Ajutement de la forme du texte à la taille de la fenêtre
        texte.adjustSize()
        texte.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        texte.setWordWrap(True)
        texte.setAlignment(Qt.AlignJustify)
        scroll_area.setWidget(texte)
        
        # Ajout dans le contenant et dans l'onglet correspondant
        zone_de_texte.addWidget(scroll_area)
        self.ongl_aide[nom_onglet][0].setLayout(zone_de_texte)

        

        
#    """
#    Onglet 3
#    """
#    def tabselection_grain(self) :
#        # Sélection de l'image à afficher #### A MODIFIER AVEC DEFILEMENT        
#        self.image_1 = "C:/Users/Maylis/Documents/1.COURS/4.ESIEE/PROJET/sable/gui/tests_Alexandre/Result1.pgm"             
#        
#        # Création d'un contenant
#        grille = QGridLayout()
#        
#        # Création d'un contenant pour l'image 
#        self.label = QLabel()
#        self.label.setFixedSize(320,320)
#        self.image_1_pixmap=QPixmap(self.image_1)
#        print("width=", self.image_1_pixmap.width(), "height=", self.image_1_pixmap.height())
#        width=self.label.width()
#        height=self.label.height()
#        self.label.setPixmap(QPixmap(self.image_1).scaled(width,height,Qt.KeepAspectRatio))      
#        self.label.mousePressEvent=self.getPixel
#        
#        
#        # Label explication onglet
#        self.label_1 = QLabel("<b>Veuillez cliquer sur le grain que vous souhaitez selectionner</b>")
#        self.label_1.setWordWrap(True)
#        self.label_1.setAlignment(Qt.AlignJustify)
#        
#                
#        # Ajout des widget dans le contenant et du contenant dans l'onglet
#        grille.addWidget(self.label,2,1)
#        grille.addWidget(self.label_1, 1,1)
#        self.selection_grain.setLayout(grille)
#        


    """
    Onglet 4
    """
    def tabaffichage_image(self) :
        # Selection des images de l'onglet        
        self.image_1 = "../tests_Alexandre/Result1.pgm"         # Image "principale"
        self.image_2 = "../tests_Alexandre/Image_btn_g.png"  	# Icone du bouton de gauche
        self.image_3 = "../tests_Alexandre/Image_btn_d.png"     # Icone du couton de droite
    
        # Box principale et secondaires contenant les objets de la fenêtre
        self.gridLayout = QGridLayout() 
        self.horizontalLayout = QHBoxLayout()#self.gridLayout)
        
        # Création d'un QLabel contenant l'image et ajout dans le contenant
        self.label=QLabel()
        self.label.setFixedSize(320,320)
        width=self.label.width()
        height=self.label.height()
        self.label.setPixmap(QPixmap(self.image_1).scaled(width,height,Qt.KeepAspectRatio))
        self.label.mousePressEvent=self.getPixel
        self.gridLayout.addWidget(self.label,1,1)
        
        
        # Création des boutons pour passer les images
        ### Bouton 1
        self.pushButton1 = QPushButton() 
        self.pushButton1.setText("Image precedente") 
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(self.image_2),QIcon.Normal, QIcon.Off)
        self.pushButton1.setIcon(icon1) 
        
        ### Bouton 2
        self.pushButton2 = QPushButton() 
        self.pushButton2.setText("Image suivante") 
        icon2 = QIcon() 
        icon2.addPixmap(QPixmap(self.image_3),QIcon.Normal, QIcon.Off)
        self.pushButton2.setIcon(icon2) 
        
        # Ajout des boutons au Layout
        self.horizontalLayout.addWidget(self.pushButton1) 
        self.horizontalLayout.addWidget(self.pushButton2) 
        self.gridLayout.addLayout(self.horizontalLayout,2,1)
        
        # Ajout dans l'onglet
        self.affichage_image.setLayout(self.gridLayout)
        

    def getPixel(self,event):
        x=event.pos().x()
        y=event.pos().y()
        print('x=', x, '   ;    y=', y)
        ## Mofifier pour colorer le grain et changer l'image avec grain coloré, aller récupérer le grain wlh
        

"""
Code principal
"""
# Fonctions et courbes que l'on veut afficher
theta = numpy.linspace(-10 * numpy.pi, 5 * numpy.pi, 100)
z = numpy.linspace(-2, 2, 100)
r = z**2 + 1
x = r * numpy.sin(theta)
y = r * numpy.cos(theta)

courbe1 = [x, y, z]
courbe2 = [y, z, x]
courbe3 = [z, x, y]
graphe = [courbe1, courbe2, courbe3]

if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = Fenetre() # Crée un objet de type Fenetre
    fenetre.setWindowTitle("Graphique 3D (DEMONSTRATION)") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    sys.exit(application.exec_()) # application.exec_() attend que tout ce qui est en cours soit exécuté