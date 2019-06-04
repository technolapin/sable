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
import re # Librairie pour faire des recherches

# Librairie Python Qt5 pour créer la GUI
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 

# Outils mathématiques
from math import *
import numpy 

# Outils de visualisation graphique
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg 
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.cm as cm 




"""
PARAMETRES
"""
ANTI_LAG = True # Désactive l'affichache multi-couches dans le mille-feuilles

NB_IMGS = 4000 # Nombre d'images au format PGM
INTERVALLE = 250 # Intervalle temporel dans cette liste d'images
URL = "C:/Users/Maylis/Documents/1.COURS/4.ESIEE/PROJET/sable/extraction/images/test-"
HAUTEUR = 80
LARGEUR = 80

"""
PARAMETRES (suite)
"""
# Graphique que on veut afficher
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
# Elle doit être une liste de listes
# Chaque sous-liste représente une courbe, et toutes ces sous-listes doivent avoir la même longueur
# Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer

if NB_IMGS % INTERVALLE != 0 :
    print( "On a un problème !" )
    sys.exit(1)


"""
Lecture d'un fichier PGM
Source : https://github.com/jmeyers314/astrophotoreduce/blob/master/pgm.py
"""
def read_pgm(filename, byteorder='>'):
    """
    Return image data from a raw PGM file as numpy array.
    Format specification: http://netpbm.sourceforge.net/doc/pgm.html
    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))




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
Classe MilleFeuille3D, hérite de FigureCanvasQTAgg
Cette classe permet de gérer un graphique 3D d'images pouvant être tourné et inséré dans un environnement Qt
Ces images sont affichées sous la forme d'un mille-feuilles
"""
class MilleFeuille3D(FigureCanvasQTAgg) :
    """
    Constructeur, initialise le graphique
    """
    def __init__(self) :
        self.figure = plt.figure()
        self.figure.subplots_adjust(bottom=0, top=1, left=0, right=1) # Supprime les marges
        FigureCanvasQTAgg.__init__( self, self.figure ) # Objet de type FigureCanvas
        self.axes = self.figure.gca( projection = '3d' ) # On lui dit qu'on veut des axes 3D, et on les stockes dans un attribut
    
    """
    Dessine ou actualise avec un nouveau graphique
    @param "listeImages" : Liste d'images à afficher, au format PGM (Base 8), associées à leur hauteur à afficher.
    """
    def dessinerMilleFeuille3D(self, listeImages) : # Procédure qui dessine le graphique      
        self.axes.clear() # Nettoie les axes et leur contenu
#        self.axes.set_aspect( 'equal' ) # Permet d'avoir un repère orthonormal

        for I in range( len( listeImages ) ) :
            # Source : https://stackoverflow.com/questions/25287861/creating-intersecting-images-in-matplotlib-with-imshow-or-other-function/25295272#25295272
            # Create a 80 x 80 vertex mesh
            X, Y = numpy.meshgrid(numpy.linspace(0,1,HAUTEUR), numpy.linspace(0,1,LARGEUR))
            Z = numpy.zeros(X.shape) + listeImages[I][1]
            
            # Source : https://stackoverflow.com/questions/45663597/plotting-3d-image-form-a-data-in-numpy-array
            # Traitement de l'image
            image = read_pgm(listeImages[I][0], byteorder='<') # Matrix au format uint8
            imageConvertie = image.astype(numpy.float64) / 255 # Convertie en float64
            T = cm.hot(imageConvertie) # Matrix float64 que facecolors peut prendre
            
            self.axes.plot_surface(X, Y, Z, facecolors=T)
        
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
        
        # Impose la taille minimale de la fenêtre, en pixels et affiche en grand écran
        self.setMinimumSize( QSize(500, 500) )
        self.setWindowState(Qt.WindowMaximized)
        
        # Création des onglets de la fenêtre
        self.setTabShape(1)
        self.visu_graph = QWidget()
        self.aide = QWidget()
      #  self.selection_grain = QWidget()  
        self.affichage_image = QWidget()
        self.millefeuille = QWidget()
        self.affichage_coupes= QWidget()

        # Dictionnaire des onglets de la fenêtre 
        self.ongl_fen = { 'visu_graph' :        [self.visu_graph,         "Visualisation du Graphique", self.tabGraphique3D()       ] , 
                          'aide' :              [self.aide ,              "Aide",                       self.tabAide()              ] , 
                          'affichage_image' :   [self.affichage_image,    "Affichage coupe 2D",         self.tabaffichage_image()   ] ,
                          'millefeuille' :      [self.millefeuille,       "Mille-feuilles" ,            self.tabmillefeuille()      ] ,
                          'affichage_coupes' :  [self.affichage_coupes,   "Affichage coupes 3D",        self.tabaffichage_coupes()  ]}
        
        
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
        self.horizontalLayout = QHBoxLayout()
        
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
        




    def tabmillefeuille(self):
        self.milleFeuille3D = MilleFeuille3D()
        
        # Défilement de couches inférieures (Valeur de la couche minimum à afficher)
        self.barreDeScrollMFCoucheMin = QScrollBar()
        self.barreDeScrollMFCoucheMin.setMaximum( INTERVALLE - 1 )
        self.barreDeScrollMFCoucheMin.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        # Défilement de couches supérieures (Valeur de la couche maximum à afficher)
        self.barreDeScrollMFCoucheMax = QScrollBar()
        self.barreDeScrollMFCoucheMax.setMaximum( INTERVALLE - 1 )
        self.barreDeScrollMFCoucheMax.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        # Défilement temporel
        self.barreDeScrollMFTemps = QScrollBar(Qt.Horizontal)
        self.barreDeScrollMFTemps.setMaximum( NB_IMGS / INTERVALLE - 1 )
        self.barreDeScrollMFTemps.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        grille = QGridLayout()
        
        grille.addWidget( self.milleFeuille3D, 2, 1 )
        grille.addWidget( self.barreDeScrollMFCoucheMin, 2, 2 )
        if not ANTI_LAG : grille.addWidget( self.barreDeScrollMFCoucheMax, 2, 3 )
        # Ne pas l'afficher quand l'ANTI_LAG est activé, donc inutilisable, donc une seule couche affichée
        grille.addWidget( self.barreDeScrollMFTemps, 3, 1 )
        
        self.dessinerMilleFeuille3D(0)
        
        self.millefeuille.setLayout( grille )

    """
    Gére le dessin et les changements du mille feuille 3D
    """
    def dessinerMilleFeuille3D(self, value) :
        listeImages = []
        if self.barreDeScrollMFCoucheMax.value() != 0 :
            for i in range(self.barreDeScrollMFCoucheMin.value(), self.barreDeScrollMFCoucheMax.value(), 1) :
                listeImages.append( [URL + str(self.barreDeScrollMFTemps.value() * INTERVALLE + i) + ".pgm", self.barreDeScrollMFCoucheMin.value() + i] )
        else : # Permet de ne commander qu'avec le défilement de la valeur minimum, forcément si ANTI_LAG activé
            numeroImage = self.barreDeScrollMFTemps.value() * INTERVALLE + self.barreDeScrollMFCoucheMin.value()
            listeImages.append( [URL + str(numeroImage) + ".pgm", self.barreDeScrollMFCoucheMin.value()] )
        
        self.milleFeuille3D.dessinerMilleFeuille3D( listeImages )
        
        print( "[Debug] Min : " + str( self.barreDeScrollMFCoucheMin.value() ) + ", Max : " + str( self.barreDeScrollMFCoucheMax.value() ) + ", Temps : " + str( self.barreDeScrollMFTemps.value() ) )
        if ANTI_LAG : print( "[Debug] Affichage : " + URL + str(numeroImage) + ".pgm" )



    def tabaffichage_coupes(self) :
        # Création d'un contenant de l'onglet
        grille=QGridLayout()


######## Images

        # Création d'un contenant pour les images 
        contenant_widget=QWidget()
        contenant_grille=QGridLayout()
        
        # Image axe (x,y)
        image_xy = "../tests_Alexandre/Result1.pgm"  
        label_image_xy = QLabel()
        label_image_xy.setFixedSize(160,160)
        width=label_image_xy.width()
        height=label_image_xy.height()
        label_image_xy.setPixmap(QPixmap(image_xy).scaled(width,height,Qt.KeepAspectRatio))

        # Image axe (y,z)
        image_yz = "../tests_Alexandre/Result1.pgm"  
        label_image_yz = QLabel()
        label_image_yz.setFixedSize(160,160)
        label_image_yz.setPixmap(QPixmap(image_yz).scaled(width,height,Qt.KeepAspectRatio))
        
        # Image axe (z,x)
        image_zx = "../tests_Alexandre/Result1.pgm"  
        label_image_zx = QLabel()
        label_image_zx.setFixedSize(160,160)
        label_image_zx.setPixmap(QPixmap(image_zx).scaled(width,height,Qt.KeepAspectRatio))
        
        # Ajout des images dans le contenant à images
        contenant_grille.addWidget(label_image_xy,5,2)
        contenant_grille.addWidget(label_image_yz,2,3)
        contenant_grille.addWidget(label_image_zx,2,1)
        contenant_widget.setLayout(contenant_grille)
        
        # Textes correspondant aux images
        texte_xy=QLabel("Image (x,y)")
        texte_yz=QLabel("Image (y,z)")
        texte_zx=QLabel("Image (z,x)")
        contenant_grille.addWidget(texte_xy,4,2)
        contenant_grille.addWidget(texte_yz,1,3)
        contenant_grille.addWidget(texte_zx,1,1)

        # Image des axes
        image_axes = "axesxyz.png"
        label_image_axes = QLabel()
        label_image_axes.setPixmap(QPixmap(image_axes))
        contenant_grille.addWidget(label_image_axes,3,2)
        
        
        # Ajout du contenant d'images dans la grille globale
        grille.addWidget(contenant_widget,2,1)
        
        
        
########### Barres de scroll      
        horizontalLayout = QGridLayout()
        
        # Scroll Bar de temps
        label_temps=QLabel("Temps")
        barreScrollTemps=QScrollBar(Qt.Horizontal)
#        barreScrollTemps.setMinimum(0)
        barreScrollTemps.setMaximum(250)

        # Scroll Bar des axes
        label_axex=QLabel("X")
        barreScrollAxeX=QScrollBar(Qt.Horizontal)
        label_axey=QLabel("Y")
        barreScrollAxeY=QScrollBar(Qt.Horizontal)
        label_axez=QLabel("Z")
        barreScrollAxeZ=QScrollBar(Qt.Horizontal)
        
        # Ajout des barres de scroll 
        horizontalLayout.addWidget(label_temps,1,1)
        horizontalLayout.addWidget(label_axex,2,1)
        horizontalLayout.addWidget(label_axey,3,1)
        horizontalLayout.addWidget(label_axez,4,1)
        horizontalLayout.addWidget(barreScrollTemps,1,2)
        horizontalLayout.addWidget(barreScrollAxeX,2,2)
        horizontalLayout.addWidget(barreScrollAxeY,3,2)
        horizontalLayout.addWidget(barreScrollAxeZ,4,2)
        grille.addLayout(horizontalLayout,2,2)

######## Positions actuelles x,y,z et temps
        valeur_temps=QLabel("Temps : 0")
        grille.addWidget(valeur_temps,1,1)








        # Ajout du contenu à l'onglet
        self.affichage_coupes.setLayout(grille)




"""
Code principal
"""

if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = Fenetre() # Crée un objet de type Fenetre
    fenetre.setWindowTitle("Graphique 3D (DEMONSTRATION)") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    sys.exit(application.exec_()) # application.exec_() attend que tout ce qui est en cours soit exécuté