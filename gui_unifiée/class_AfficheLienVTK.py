"""
Basé sur ce script : https://stackoverflow.com/questions/48105646/embedding-vtk-object-in-pyqt5-window
@author Maylis / Amaury
"""

import sys
import vtk
from PyQt5 import QtCore, QtGui
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFrame, QVBoxLayout, QScrollBar, QLabel

from vtk import vtkNamedColors, vtkRenderer, vtkPolyDataReader, vtkPolyDataMapper, vtkActor
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class AfficheLienVTK(QGridLayout):

    def __init__(self, parent = None):
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
#        fichierVTK = lienVTK
#        reader = vtkPolyDataReader()
#        reader.SetFileName(fichierVTK)
#        reader.Update()
#        
#        # Create a mapper
        self.mapper = vtk.vtkPolyDataMapper()
#        mapper.SetInputConnection(reader.GetOutputPort())
#        
        # Create an actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(self.colors.GetColor3d('Tan'))

        self.ren.AddActor(self.actor)
        self.ren.SetBackground(self.colors.GetColor3d('White'))
        self.ren.ResetCamera()

        self.frame.setLayout(self.vl)
        self.addWidget(self.frame)
        self.iren.Initialize()
        self.iren.Start()

    def AfficherNouveauVTK(self, lienVTK=None):
        reader = vtkPolyDataReader()
        reader.SetFileName(lienVTK)
        reader.Update()
        self.mapper.SetInputConnection(reader.GetOutputPort())
        self.actor.SetMapper(self.mapper)
        self.ren.ResetCamera()
        self.iren.Initialize()