import os
import sys
from time import sleep

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QScrollBar, QLabel

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from functions_urlDesFichiersTraites import *

from threading import Thread, Semaphore


"""
Variables globales
"""
# Liste des actors à afficher
actors = []

# Liste de booléens, si les actors sont initialisés
initActors = []

# Verrou à la liste des actors
semActors = Semaphore()


"""
Thread de chargement des VTKs dans la liste actors
"""
class Chargeur(Thread) :
    def __init__(self) :
        Thread.__init__(self)

    def run(self) :
        self.colors = vtk.vtkNamedColors() # Pour pouvoir mettre des couleurs
        
        for instantTemporel in range( int(nombreInstantsTemporels()) + 1 ) :
            fichierVTK = genererURLdesVTK( instantTemporel )
            
            if not os.path.isfile( fichierVTK ) :
                print ( "[Erreur TabVTK] " + fichierVTK + " n'existe pas !" )
            
            print ( "[Info TabVTK] Chargement : " + fichierVTK)
            
            # Create source
            # Source : https://lorensen.github.io/VTKExamples/site/Python/IO/ReadVTP/
            reader = vtk.vtkPolyDataReader()
            reader.SetFileName(fichierVTK)
            reader.Update()
            
            # Create a mapper
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(reader.GetOutputPort())
            
            # Create an actor
            semActors.acquire()
            initActors[instantTemporel] = True
            actors[instantTemporel].SetMapper(mapper)
            actors[instantTemporel].GetProperty().SetColor(self.colors.GetColor3d('Tan')) # Couleur de l'objet 3D
            semActors.release()

"""
Classe TabVTK, hérite de la classe QGridLayout, c'est donc une grille
Cette classe représente le contenu d'une fenêtre PyQt
Elle peut donc aussi être utilisée comme un onglet dans une fenêtre
Basé sur ce script : https://stackoverflow.com/questions/48105646/embedding-vtk-object-in-pyqt5-window
"""
class TabVTK(QGridLayout) :
    """
    Constructeur, crée le contenu de l'onglet
    """
    def __init__(self, parent=None) :
        super(TabVTK, self).__init__(parent) # Appel du constructeur de QGridLayout
        
        """
        Divers
        """
        # Défilement temporel
        self.barreDeScrollTemps = QScrollBar(Qt.Horizontal)
        self.barreDeScrollTemps.setMaximum( nombreInstantsTemporels() )
        self.barreDeScrollTemps.valueChanged.connect( self.dessinerVTK )
        self.addWidget( self.barreDeScrollTemps, 2, 1 )
        
        """
        VTK
        """
        self.colors = vtk.vtkNamedColors() # Pour pouvoir mettre des couleurs
        
        self.frame = QFrame()
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        
        
        # Ajout Maylis
        vertical_layout=QVBoxLayout()
        self.valeur_temps=QLabel("Temps : 0")
        vertical_layout.addWidget(self.valeur_temps)
        vertical_layout.addWidget(self.frame, stretch=2)
        self.addLayout(vertical_layout,1,1)
        # Fin Ajout Maylis
        
        
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        
        # Remplissage de la liste avec du vide
        for instantTemporel in range( int(nombreInstantsTemporels()) + 1 ) :
            actors.append( vtk.vtkActor() )
            initActors.append( False )
        
        self.actorPrecedent = self.barreDeScrollTemps.value()
        self.dessinerVTK(0)
        
        self.ren.SetBackground(self.colors.GetColor3d('White')) # Couleur du fond
#        self.ren.ResetCamera()
        
        self.frame.setLayout(self.vl)
#        self.addWidget(self.frame, 1, 1)
        
#        self.iren.Initialize()
        self.iren.Start()
        
        # Remplissage avec les VTKs
        thread = Chargeur()
        thread.start()
    
    """
    Gère le dessin et les changements du VTK
    """
    def dessinerVTK(self, value) :
        instantTemporel = self.barreDeScrollTemps.value()
        print ( "[Debug TabVTK] Affichage : " + genererURLdesVTK( instantTemporel ) )
        
        # Ajout Maylis
        self.valeur_temps.setText("Temps : " + str(instantTemporel))
        # Fin Ajout Maylis
        
        semActors.acquire()
        if initActors[self.actorPrecedent] :
            self.ren.RemoveActor( actors[self.actorPrecedent] )
        if initActors[instantTemporel] :
            self.ren.AddActor( actors[instantTemporel] )
        self.actorPrecedent = instantTemporel
        semActors.release()
        self.iren.Initialize()


"""
Code principal pour démonstration
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = QWidget() # Crée un objet de type QWidget
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.setLayout( TabVTK() )
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté
