import sys

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QScrollBar

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from parametres import *


FICHIER = "../amaury/tests/test.vtk"


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
        self.barreDeScrollTemps.setMaximum( NB_IMGS / INTERVALLE_XY - 1 )
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
        
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        
        self.actor = vtk.vtkActor()
        self.dessinerVTK(0)
        
        self.ren.SetBackground(self.colors.GetColor3d('White')) # Couleur du fond
#        self.ren.ResetCamera()
        
        self.frame.setLayout(self.vl)
        self.addWidget(self.frame, 1, 1)
        
        self.iren.Initialize()
        self.iren.Start()
    
    """
    Gère le dessin et les changements du VTK
    """
    def dessinerVTK(self, value) :
        tempsFormate = format(self.barreDeScrollIRMTemps.value(), '02d') # String sur 2 digits
        fichierVTK = URL_POUR_VTK + tempsFormate + ".vtk"
        
        if not os.path.isfile( fichierVTK ) :
            print ( "[Erreur TabVTK] " + fichierVTK + " n'existe pas !" )
        
        
        self.ren.RemoveActor(self.actor)
        
        # Create source
        # Source : https://lorensen.github.io/VTKExamples/site/Python/IO/ReadVTP/
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(fichierVTK)
        reader.Update()
        
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        
        # Create an actor
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(self.colors.GetColor3d('Tan')) # Couleur de l'objet 3D
        
        self.ren.AddActor(self.actor)


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
