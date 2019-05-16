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
        super(Fenetre, self).__init__(parent) # Appel du constructeur de QWidget
        
        # Impose la taille minimale de la fenêtre, en pixels
        self.setMinimumSize( QSize(500, 500) );
        
        # Création des onglets de la fenêtre
        self.setTabShape(1)
        self.onglet1 = QWidget()
        self.onglet2 = QWidget()
        self.onglet3 = QWidget()  
        
        # Ajout des onglets à la fenêtre  	    
        self.addTab( self.onglet1, "Visualisation du Graphique" ) 
        self.addTab( self.onglet2, "Aide" )
        self.addTab( self.onglet3, "Onglet 3" )
        
        # Appel des procédures qui remplissent les onglets
        self.tabGraphique3D()
        self.tabAide()
        self.tabOnglet3()
    
    

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
        
        self.onglet1.setLayout( grille ) # Ajout du contenu dans l'onglet


    """
    Gère les changements par l'utilisateur dans le menu déroulant de sélection
    """
    def changementGraphique3D(self, value) :
         self.graphique3D.dessinerGraphique3D( graphe, self.barreDeScrollCourbes.value(), self.barreDeScrollTemps.value() )
         print( "[Debug] Temps : " + str( self.barreDeScrollCourbes.value() ) + ", Courbe : " + str( self.barreDeScrollTemps.value() ) + ", Valeur donnée : " + str( value ) )


    
    
    
    """
    Onglet 2
    """
    def tabAide(self) :
        layout=QGridLayout()

        # Création d'onglets dans la page d'aide
        onglets = QTabWidget()
        intro_onglet = QWidget()
        aide_onglet1 = QWidget()
        aide_onglet2 = QWidget()
        onglets.addTab( intro_onglet, "Introduction" ) 
        onglets.addTab( aide_onglet1, "Onglet 2" )
        onglets.addTab( aide_onglet2, "Onglet 3" )
        onglets.setTabPosition(2)
        onglets.setTabShape(1)
        
        # Ajout des onglets dans la grille et l'onglet Aide
        layout.addWidget(onglets)
        self.onglet2.setLayout(layout)
        
        
        # Contenu de l'onglet  d'introduction
        zone_de_texte = QHBoxLayout()
        scroll_area=QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        
        fichier=codecs.open("Aide_generale.html", 'r',encoding='utf-8')
        texte=QLabel(fichier.read())
        texte.adjustSize()
        texte.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        texte.setWordWrap(True)
        texte.setAlignment(Qt.AlignJustify)
        scroll_area.setWidget(texte)
        zone_de_texte.addWidget(scroll_area)
        intro_onglet.setLayout(zone_de_texte)



        
    """
    Onglet 3
    """
    def tabOnglet3(self) :
        grille = QGridLayout()
        
        self.onglet3.setLayout( grille )
    
 



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