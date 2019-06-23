"""
Basé sur ce script : https://stackoverflow.com/questions/48105646/embedding-vtk-object-in-pyqt5-window
@author Amaury
"""

import sys
import vtk
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QScrollBar, QLabel

from vtk import vtkNamedColors, vtkRenderer, vtkPolyDataReader, vtkPolyDataMapper, vtkActor
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class AfficheLienVTK(QGridLayout):

    def __init__(self, lienVTK ,parent = None):
        super(AfficheLienVTK, self).__init__(parent)
        
        self.colors = vtkNamedColors()

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source
        fichierVTK = lienVTK
        reader = vtkPolyDataReader()
        reader.SetFileName(fichierVTK)
        reader.Update()
        
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(self.colors.GetColor3d('Tan'))

        self.ren.AddActor(actor)
        self.ren.SetBackground(self.colors.GetColor3d('White'))
        self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.addWidget(self.frame)
       # self.show()
        self.iren.Initialize()
        self.iren.Start()


if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = QWidget() # Crée un objet de type QWidget
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.setLayout( AfficheLienVTK(lienVTK="../extraction/vtk_3D/vtk_t_01.vtk" ))
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté