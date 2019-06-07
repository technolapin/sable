"""
Environnement graphique d'affichage de graphiques en 3D
Utilise la librairie PyQt pour l'UI, et MatPlotLib pour les graphiques
Ce code est basé sur un code trouvé sur StackOverflow.com qui correspondait à ce que nous voulions faire
Source : https://stackoverflow.com/questions/52379426/pyqta-matplotlib-how-to-redraw-update-a-3d-surface-plot-in-a-window
Auteurs originaux :
- "Sreeletha" : https://stackoverflow.com/users/10374297/sreeletha
- "Joe" : https://stackoverflow.com/users/7919597/joe
"""


import sys # Librairie pour faire des appels systèmes
from PyQt4.QtCore import * # Librairie Python Qt4 pour créer la GUI
from PyQt4.QtGui import * # Librairie Python Qt4 pour créer la GUI

from math import * # Librairie mathématique, pour utiliser la fonction log()
import numpy # Autre librairie mathématique

from matplotlib.figure import Figure # Classe Figure de la librairie Matplotlib
import matplotlib.pyplot as plt # Librairie pour faire des graphiques
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg # Classe pour mettre du Matplotlib dans Qt
from mpl_toolkits.mplot3d import Axes3D # Classe pour gérer les axes 3D

from random import choice # Fonction pour chosir aléatoirement un élement dans une liste


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
        self.figure = plt.figure(figsize=(7,7)) # Crée un objet de type Figure
        FigureCanvasQTAgg.__init__(self, self.figure) # Objet de type FigureCanvas
        self.axes = self.figure.gca(projection='3d') # On lui dit qu'on veut des axes 3D, et on les stockes dans un attribut
    
    """
    Dessine ou actualise avec un nouveau graphique
    Le paramètre "liste" est une liste de listes
    Chaque sous-liste représente une courbe
    Ces sous-listes doivent comprendre 3 sous-sous-listes étant les coordonnées X, Y et Z à tracer
    """
    def dessinerGraphique3D(self, liste) : # Procédure qui dessine le graphique
        self.axes.clear() # Nettoie les axes
        self.axes.set_xlabel('Axe X') # Label sur l'axe X
        self.axes.set_ylabel('Axe Y') # Label sur l'axe Y
        self.axes.set_zlabel('Axe Z') # Label sur l'axe Z
        self.axes.set_aspect('equal') # Permet d'avoir un repère orthonormal
        for courbe in liste :
            couleur = choice(["b", "g", "r", "c", "m", "y"]) # Choisi aléatoirement dans la liste des couleurs de base de Matplotlib
            self.axes.plot(courbe[0], courbe[1], courbe[2], couleur + 'o-') # Dessine le graphique 3D à partir de 3 listes dans les axes
        self.draw() # Dessine le graphique 3D avec les axes

"""
Classe Fenetre, hérite de la classe QWidget
Cette classe permet de gérer la fenêtre Qt
Le graphique 3D est inséré dedans
"""
class Fenetre(QWidget) :
    """
    Constructeur
    """
    def __init__(self, parent=None) :
        super(Fenetre, self).__init__(parent) # Appel du constructeur de QWidget
        
#        self.menuSelection = QComboBox() # Crée un objet de type QComboBox, c'est un menu déroulant
#        self.menuSelection.addItems(['Graph1', 'Graph2']) # Ajoute les indexes de ce menu
#        self.menuSelection.currentIndexChanged.connect(self.changementGraphique3D) # La procédure à appeler lors du changement
        
        self.graphique3D = Graphique3D() # Crée un objet de type Graphique3D
        self.graphique3D.setMinimumSize(QSize(400, 400)) # Définit la taille minimum en pixels de ce Widget
        # Cela permet de bloquer le trop retrécissement de la fenêtre
        # On peut remplacer "QSize(400, 400)" par "self.graphique3D.sizeHint()" pour que la taille par défaut soit la taille minimum
        
        # Défilement temporel
        self.barreDeScroll1 = QScrollBar() # CRée un objet de type QScrollBar, c'est une barre de défilement
        self.barreDeScroll1.setMaximum( len(graphe[0][0]) ) # Défini le nombre de valeurs qu'on peut y parcourir
        self.barreDeScroll1.sliderMoved.connect(self.changementGraphique3D) # La procédure à appeler lorsque l'utilisateur y touche
        
        # Défilement coupes
        self.barreDeScroll2 = QScrollBar() # CRée un objet de type QScrollBar, c'est une barre de défilement
        self.barreDeScroll2.setMaximum(255) # Défini le nombre de valeurs qu'on peut y parcourir
        self.barreDeScroll2.sliderMoved.connect(self.changementGraphique3D) # La procédure à appeler lorsque l'utilisateur y touche
        
        grille = QGridLayout() # Crée un objet de type QGridLayout, c'est l'intérieur de la fenêtre, une grille ("layout")
        
#        grille.addWidget(self.menuSelection, 1, 1) # Ajoute le menu déroulant en position ligne 2 colonne 1
        grille.addWidget(self.graphique3D, 2, 1) # Ajoute le graphique 3D en position ligne 2 colonne 1
        grille.addWidget(self.barreDeScroll1, 2, 2) # Ajoute la barre de défilement 1 en position ligne 2 colonne 2
        grille.addWidget(self.barreDeScroll2, 2, 3) # Ajoute la barre de défilement 2 en position ligne 2 colonne 2
        
        self.setLayout(grille) # Definit notre grille comme grille à utiliser
        
        self.graphique3D.dessinerGraphique3D( graphe ) # Afficher graphique de base
    
    """
    Gère les changements par l'utilisateur dans le menu déroulant de sélection
    """
    def changementGraphique3D(self) :
#        graphiqueDemande = str(self.menuSelection.currentText())
#        if graphiqueDemande == "Graph1" :
#            self.graph1()
#        if graphiqueDemande == "Graph2" :
#            self.graph2()
         self.barreDeScroll1.value()


"""
Code principal
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

# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = Fenetre() # Crée un objet de type Fenetre
    fenetre.setWindowTitle("Graphique 3D (DÉMONSTRATION)") # Définit le nom de la fenêtre
    fenetre.show() # Affiche la fenêtre
    sys.exit(application.exec_()) # application.exec_() attend que tout ce qui est en cours soit exécuté