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


"""
PARAMETRES
"""
ANTI_LAG = True # Désactive l'affichache multi-couches dans le mille-feuilles

NB_IMGS = 4000 # Nombre d'images au format PGM
INTERVALLE_XY = 250 # Intervalle temporel dans cette liste d'images
URL_POUR_MF = "../extraction/images/test-"

URL_POUR_IRM = "../extraction/coupes_3D/"
INTERVALLE_XZ = 80
INTERVALLE_YZ = 80



"""
IMPORTATIONS
"""
import os # Librairie d'interface avec l'OS
import sys # Librairie pour faire des appels systèmes

from PyQt5.QtCore import * # Librairie Python Qt4 pour créer la GUI
from PyQt5.QtGui import * # Librairie Python Qt4 pour créer la GUI
from PyQt5.QtWidgets import * # Librairie Python Qt4 pour créer la GUI

from math import * # Librairie mathématique, pour utiliser la fonction log()
import numpy # Autre librairie mathématique

from matplotlib.figure import Figure # Classe Figure de la librairie Matplotlib
import matplotlib.pyplot as plt # Librairie pour faire des graphiques
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg # Classe pour mettre du Matplotlib dans Qt
from mpl_toolkits.mplot3d import Axes3D # Classe pour gérer les axes 3D
import matplotlib.cm as cm # Pour cm.hot()

from random import choice # Fonction pour choisir aléatoirement un élement dans une liste
import re # Librairie pour faire des recherches



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

if NB_IMGS % INTERVALLE_XY != 0 :
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




# Note : Une variable commencant par "self." est un attribut de l'objet
"""
Classe Graphique3D, hérite de FigureCanvasQTAgg
Cette classe permet de gérer un graphique 3D Matplotlib pouvant être tourné et inséré dans un environnement Qt
"""
class Graphique3D(FigureCanvasQTAgg) :
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
    Le paramètre "liste" est une liste de listes
    Chaque sous-liste représente une courbe
    Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
    @param "courbeAfficher" : La courbe à afficher dans "liste" + 1, 0 si il faut les afficher toutes
    @param "tempsAfficher" : L'instant à afficher dans "liste" + 1, 0 si il faut afficher tous les instants
    """
    def dessinerGraphique3D(self, liste, courbeAfficher, tempsAfficher) : # Procédure qui dessine le graphique
        self.axes.clear() # Nettoie les axes et leur contenu
        self.axes.set_xlabel( 'Axe X' ) # Label sur l'axe X
        self.axes.set_ylabel( 'Axe Y' ) # Label sur l'axe Y
        self.axes.set_zlabel( 'Axe Z' ) # Label sur l'axe Z
#        self.axes.set_aspect( 'equal' ) # Permet d'avoir un repère orthonormal
        if courbeAfficher != 0 :
            couleur = choice( ["b", "g", "r", "c", "m", "y"] ) # Choisi aléatoirement dans la liste des couleurs de base de Matplotlib
            self.axes.plot( liste[courbeAfficher - 1][0], liste[courbeAfficher - 1][1], liste[courbeAfficher - 1][2], couleur + 'o-' ) # Dessine le graphique 3D à partir de 3 listes dans les axes
        else :
            for courbe in liste :
                couleur = choice( ["b", "g", "r", "c", "m", "y"] ) # Choisi aléatoirement dans la liste des couleurs de base de Matplotlib
                self.axes.plot( courbe[0], courbe[1], courbe[2], couleur + 'o-' ) # Dessine le graphique 3D à partir de 3 listes dans les axes
        self.draw() # Dessine le graphique 3D avec les axes

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
    @param "listeImages" : Liste d'images à afficher, au format PGM (Base 8), associées à leur hauteur à afficher
    """
    def dessinerMilleFeuille3D(self, listeImages) : # Procédure qui dessine le graphique      
        self.axes.clear() # Nettoie les axes et leur contenu
        self.axes.set_xlabel( 'Axe X' ) # Label sur l'axe X
        self.axes.set_ylabel( 'Axe Y' ) # Label sur l'axe Y
        self.axes.set_zlabel( 'Axe Z' ) # Label sur l'axe Z
#        self.axes.set_aspect( 'equal' ) # Permet d'avoir un repère orthonormal

        for I in range( len( listeImages ) ) :
            if os.path.isfile( listeImages[I][0] ) : # Si le chemin d'accès à l'image existe
                # Source : https://stackoverflow.com/questions/45663597/plotting-3d-image-form-a-data-in-numpy-array
                # Traitement de l'image
                image = read_pgm(listeImages[I][0], byteorder='<') # Matrix au format uint8
                imageConvertie = image.astype(numpy.float64) / 255 # Convertie en float64
                T = cm.gist_gray(imageConvertie) # Matrix float64 que facecolors peut prendre
                # Liste des colormaps disponibles sur matplotlib.cm :
                # https://matplotlib.org/3.1.0/gallery/color/colormap_reference.html
                
                # Source : https://stackoverflow.com/questions/25287861/creating-intersecting-images-in-matplotlib-with-imshow-or-other-function/25295272#25295272
                # Create a vertex mesh
                X, Y = numpy.meshgrid(numpy.linspace(0, len(image)-2, len(image)-1 ), numpy.linspace(0, len(image[0])-2, len(image[0])-1 ))
                Z = numpy.zeros(X.shape) + listeImages[I][1]
                
                self.axes.plot_surface(X, Y, Z, facecolors=T)
                
                print( "[Debug MF] Ajout : " + listeImages[I][0] )
            
            else :
                print( "[Erreur MF] " + listeImages[I][0] + " n'existe pas !" )
        
        self.draw()

"""
Classe MilleFeuilleIRM, hérite de FigureCanvasQTAgg
Cette classe permet de gérer un graphique 3D d'images pouvant être tourné et inséré dans un environnement Qt
Ces images sont affichées sous la forme de 3 plans perpidenculaires, similaire à un IRM
"""
"""
PROBLEME INSOLVABLE :
En fait, les 3 coupes s'affichent les unes sur les autres, il n'est pas possible qu'elles s'emelent proprement
En fait, MatPlotLib dessine chaque couche une par une... Donc c'est mort !
SOURCE : https://stackoverflow.com/questions/13932150/matplotlib-wrong-overlapping-when-plotting-two-3d-surfaces-on-the-same-axes
"""
class MilleFeuilleIRM(FigureCanvasQTAgg) :
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
    @param "imageX" : Liste contenant une image au format PGM (Base 8) à afficher dans un plan YZ, ainsi que sa position en X.
    @param "imageY" : Liste contenant une image au format PGM (Base 8) à afficher dans un plan XZ, ainsi que sa position en Y.
    @param "imageZ" : Liste contenant une image au format PGM (Base 8) à afficher dans un plan XY, ainsi que sa position en Z.
    """
    def dessinerMilleFeuilleIRM(self, imageX, imageY, imageZ) : # Procédure qui dessine le graphique      
        self.axes.clear() # Nettoie les axes et leur contenu
        self.axes.set_xlabel( 'Axe X' ) # Label sur l'axe X
        self.axes.set_ylabel( 'Axe Y' ) # Label sur l'axe Y
        self.axes.set_zlabel( 'Axe Z' ) # Label sur l'axe Z
        self.axes.set_aspect( 'equal' ) # Permet d'avoir un repère orthonormal
        
        """ Plan en YZ (Pour imageX) """
        if os.path.isfile( imageX[0] ) : # Si le chemin d'accès à l'image existe
            # Traitement de l'image
            image = read_pgm("../extraction/coupes_3D/y_z/00/t_00coupe_yz_0017.pgm", byteorder='<') # Matrix au format uint8
            imageConvertie = image.astype(numpy.float64) / 255 # Convertie en float64
            T = cm.gist_gray(imageConvertie) # Matrix float64 que facecolors peut prendre
            
            # Create a vertex mesh
            Y, Z = numpy.meshgrid(numpy.linspace(0, len(image[0])-2, len(image[0])-1 ), numpy.linspace(0, len(image)-2, len(image)-1 ))
            X = numpy.zeros(Y.shape) + imageX[1]
            
            self.axes.plot_surface(X, Y, Z, facecolors=T)
            
            print( "[Debug IRM] Ajout : " + imageX[0] )
            
        else :
            print( "[Erreur IRM] " + imageX[0] + " n'existe pas !" )
        
        """ Plan en XZ (Pour imageY) """
        if os.path.isfile( imageY[0] ) : # Si le chemin d'accès à l'image existe
            # Traitement de l'image
            image = read_pgm(imageY[0], byteorder='<') # Matrix au format uint8
            imageConvertie = image.astype(numpy.float64) / 255 # Convertie en float64
            T = cm.gist_gray(imageConvertie) # Matrix float64 que facecolors peut prendre
            
            # Create a vertex mesh
            X, Z = numpy.meshgrid(numpy.linspace(0, len(image[0])-2, len(image[0])-1 ), numpy.linspace(0, len(image)-2, len(image)-1 ))
            Y = numpy.zeros(X.shape) + imageY[1]
            
            self.axes.plot_surface(X, Y, Z, facecolors=T)
            
            print( "[Debug IRM] Ajout : " + imageY[0] )
            
        else :
            print( "[Erreur IRM] " + imageY[0] + " n'existe pas !" )
        
        """ Plan en XY (Pour imageZ) """
        if os.path.isfile( imageZ[0] ) : # Si le chemin d'accès à l'image existe
            # Traitement de l'image
            image = read_pgm(imageZ[0], byteorder='<') # Matrix au format uint8
            imageConvertie = image.astype(numpy.float64) / 255 # Convertie en float64
            T = cm.gist_gray(imageConvertie) # Matrix float64 que facecolors peut prendre
            
            # Create a vertex mesh
            X, Y = numpy.meshgrid(numpy.linspace(0, len(image)-2, len(image)-1 ), numpy.linspace(0, len(image[0])-2, len(image[0])-1 ))
            Z = numpy.zeros(X.shape) + imageZ[1]
            
            self.axes.plot_surface(X, Y, Z, facecolors=T)
            
            print( "[Debug IRM] Ajout : " + imageZ[0] )
            
        else :
            print( "[Erreur IRM] " + imageZ[0] + " n'existe pas !" )
        
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
                          'millefeuille' :      [self.millefeuille,       "Mille-feuilles" ,            self.tabMilleFeuille3D()      ] ,
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
    Onglet du mille-feuilles 3D
    """
    def tabMilleFeuille3D(self) :
        self.milleFeuille3D = MilleFeuille3D()
        
        # Défilement de couches inférieures (Valeur de la couche minimum à afficher)
        self.barreDeScrollMFCoucheMin = QScrollBar()
        self.barreDeScrollMFCoucheMin.setMaximum( INTERVALLE_XY - 1 )
        self.barreDeScrollMFCoucheMin.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        # Défilement de couches supérieures (Valeur de la couche maximum à afficher)
        self.barreDeScrollMFCoucheMax = QScrollBar()
        self.barreDeScrollMFCoucheMax.setMaximum( INTERVALLE_XY - 1 )
        self.barreDeScrollMFCoucheMax.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        # Défilement temporel
        self.barreDeScrollMFTemps = QScrollBar(Qt.Horizontal)
        self.barreDeScrollMFTemps.setMaximum( NB_IMGS / INTERVALLE_XY - 1 )
        self.barreDeScrollMFTemps.valueChanged.connect( self.dessinerMilleFeuille3D )
        
        grille = QGridLayout()
        
        grille.addWidget( self.milleFeuille3D, 2, 1 )
        grille.addWidget( self.barreDeScrollMFCoucheMin, 2, 2 )
        if not ANTI_LAG : grille.addWidget( self.barreDeScrollMFCoucheMax, 2, 3 )
        # Ne pas l'afficher quand l'ANTI_LAG est activé, donc inutilisable, donc une seule couche affichée
        grille.addWidget( self.barreDeScrollMFTemps, 3, 1 )
        
        self.dessinerMilleFeuille3D(0)
        
        self.onglet2.setLayout( grille )
    
    """
    Onglet du mille-feuilles IRM
    """
    def tabMilleFeuilleIRM(self) :
        self.milleFeuilleIRM = MilleFeuilleIRM()
        
        # Défilement de la couche X
        self.barreDeScrollIRMCoucheX = QScrollBar()
        self.barreDeScrollIRMCoucheX.setMaximum( INTERVALLE_YZ - 1 )
        self.barreDeScrollIRMCoucheX.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        # Défilement de la couche Y
        self.barreDeScrollIRMCoucheY = QScrollBar()
        self.barreDeScrollIRMCoucheY.setMaximum( INTERVALLE_XZ - 1 )
        self.barreDeScrollIRMCoucheY.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        # Défilement de la couche Z
        self.barreDeScrollIRMCoucheZ = QScrollBar()
        self.barreDeScrollIRMCoucheZ.setMaximum( INTERVALLE_XY - 1 )
        self.barreDeScrollIRMCoucheZ.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        # Défilement temporel
        self.barreDeScrollIRMTemps = QScrollBar(Qt.Horizontal)
        self.barreDeScrollIRMTemps.setMaximum( NB_IMGS / INTERVALLE_XY - 1 )
        self.barreDeScrollIRMTemps.valueChanged.connect( self.dessinerMilleFeuilleIRM )
        
        grille = QGridLayout()
        
        grille.addWidget( self.milleFeuilleIRM, 2, 1 )
        grille.addWidget( self.barreDeScrollIRMCoucheX, 2, 2 )
        grille.addWidget( self.barreDeScrollIRMCoucheY, 2, 3 )
        grille.addWidget( self.barreDeScrollIRMCoucheZ, 2, 4 )
        grille.addWidget( self.barreDeScrollIRMTemps, 3, 1 )
        
        self.dessinerMilleFeuilleIRM(0)
        
        self.onglet3.setLayout( grille )

    """
    Gère le dessin et les changements du mille-feuilles 3D (Onglet 2)
    """
    def dessinerMilleFeuille3D(self, value) :
        # Si ANTI_LAG est activé, ET/OU que barreDeScrollMFCoucheMax est à 0 (Forcément si ANTI_LAG), on ne commande qu'avec barreDeScrollMFCoucheMin
        listeImages = [] # Liste des images que on veut afficher dans le mille-feuilles
        if self.barreDeScrollMFCoucheMax.value() != 0 : # Commander le défilement avec les deux barres
            for i in range(self.barreDeScrollMFCoucheMin.value(), self.barreDeScrollMFCoucheMax.value(), 1) :
                urlImage = URL_POUR_MF + str(self.barreDeScrollMFTemps.value() * INTERVALLE_X + i) + ".pgm" # Chemin de l'image
                hauteurImage = self.barreDeScrollMFCoucheMin.value() + i # Hauteur de l'image dans le mille-feuille
                listeImages.append( [urlImage, hauteurImage] )
        else : # Permet de ne commander qu'avec le défilement de la valeur minimum, forcément si ANTI_LAG activé
            numeroImage = self.barreDeScrollMFTemps.value() * INTERVALLE_XY + self.barreDeScrollMFCoucheMin.value()
            listeImages.append( [URL_POUR_MF + str(numeroImage) + ".pgm", self.barreDeScrollMFCoucheMin.value()] )
        
        self.milleFeuille3D.dessinerMilleFeuille3D( listeImages )
        
        print( "[Debug MF] Min : " + str( self.barreDeScrollMFCoucheMin.value() ) + ", Max : " + str( self.barreDeScrollMFCoucheMax.value() ) + ", Temps : " + str( self.barreDeScrollMFTemps.value() ) )
        if ANTI_LAG : print( "[Debug MF] Affichage : " + URL_POUR_MF + str(numeroImage) + ".pgm" )
        
    """
    Gère le dessin et les changements de l'affichage IRM (Onglet 3)
    """
    def dessinerMilleFeuilleIRM(self, value) :
        coucheXFormate = format(self.barreDeScrollIRMCoucheX.value(), '04d') # String sur 4 digits
        coucheYFormate = format(self.barreDeScrollIRMCoucheY.value(), '04d') # String sur 4 digits
        coucheZFormate = format(self.barreDeScrollIRMCoucheZ.value(), '04d') # String sur 4 digits
        tempsFormate = format(self.barreDeScrollIRMTemps.value(), '02d') # String sur 2 digits
        
        imageX = URL_POUR_IRM + "y_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_yz_" + coucheXFormate + ".pgm"
        imageY = URL_POUR_IRM + "x_z/" + tempsFormate + "/t_" + tempsFormate + "coupe_xz_" + coucheYFormate + ".pgm"
        imageZ = URL_POUR_IRM + "x_y/" + tempsFormate + "/t_" + tempsFormate + "coupe_xy_" + coucheZFormate + ".pgm"
        
        self.milleFeuilleIRM.dessinerMilleFeuilleIRM( [imageX, self.barreDeScrollIRMCoucheX.value() ],
                                                      [imageY, self.barreDeScrollIRMCoucheY.value() ], 
                                                      [imageZ, self.barreDeScrollIRMCoucheZ.value() ] )
        
        print( "[Debug IRM] X : " + str( self.barreDeScrollIRMCoucheX.value() ) + ", Y : " + str( self.barreDeScrollIRMCoucheY.value() ) + ", Z : " + str( self.barreDeScrollIRMCoucheZ.value() ) + ", Temps : " + str( self.barreDeScrollIRMTemps.value() ) )
        print( "[Debug IRM] Affichage : " + imageX + ", " + imageY + ", " + imageZ )


    def tabaffichage_coupes(self) :
        grille=QGridLayout()
        
        barreScrollTemps=QScrollBar(Qt.Horizontal)
        barreScrollTemps.setMinimum(0)
        barreScrollTemps.setMaximum(250)
#        temps=barreScrollTemps.value()
#        
#        barreScrollTemps.valueChanged(temps)
#        
        barreScrollAxeX=QScrollBar(Qt.Horizontal)
        barreScrollAxeY=QScrollBar(Qt.Horizontal)
        barreScrollAxeZ=QScrollBar(Qt.Horizontal)
        
        grille.addWidget(barreScrollTemps)
        grille.addWidget(barreScrollAxeX)
        grille.addWidget(barreScrollAxeY)
        grille.addWidget(barreScrollAxeZ)
#        print(temps)
        
        self.affichage_coupes.setLayout(grille)




"""
Fonction de validation du fichier demandé
"""
# TODO : A améliorer !
def validationFichier( fichier ) :
    if fichier == "" :
        return False
    return True

"""
Fonction de traitement d'image (Appel tout le travail de traitement d'image)
"""
def traitementImage( fichier ) :
    return

"""
Code principal
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    
    fileDialog = QFileDialog() # Crée un objet de type QFileDialog (Fenêtre pour choisir un fichier)
    fileDialog.setWindowTitle("Veuillez choisir le fichier TIFF") # Définit le nom de la fenêtre
    fileDialog.show() # Affiche la fenêtre
    fichierDemande = fileDialog.getOpenFileName()[0] # Permet aussi d'attendre qu'il y ait un fichier demandé
    print( "[Debug] Fichier demandé : " + fichierDemande )
    fileDialog.close() # Fermer la fenêtre
    
    if not validationFichier( fichierDemande ) : # Si la validation de ce fichier échoue
        QMessageBox.about(None, "Information", "Ce fichier est invalide !")
    else :
        traitementImage( fichierDemande )
        
        fenetre = Fenetre() # Crée un objet de type Fenetre
        fenetre.setWindowTitle("Graphique 3D (DÉMONSTRATION)") # Définit le nom de la fenêtre
        fenetre.show() # Affiche la fenêtre
        application.exec_() # Attendre que tout ce qui est en cours soit exécuté

# EOF