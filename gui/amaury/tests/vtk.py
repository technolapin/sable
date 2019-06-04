import os

def command(cmd):
    os.system("../pink/linux/bin/"+cmd)

#command("pgm2vtk minimas.pgm 1 test.vtk")


#♣ SOURCE : https://vtk.org/Wiki/VTK/Examples/Python/Widgets/EmbedPyQt2



import sys
import vtk
from PyQt5.QtCore import * # Librairie Python Qt4 pour créer la GUI
from PyQt5.QtGui import * # Librairie Python Qt4 pour créer la GUI
from PyQt5.QtWidgets import * # Librairie Python Qt4 pour créer la GUI
#import vtk.qt.PyQtImpl
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 553)
        self.centralWidget = QWidget(MainWindow)
        self.gridlayout = QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
 
class SimpleView(QMainWindow):
 
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        
        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)
         
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
         
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.ren.AddActor(actor)
 
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    window = SimpleView()
    window.show()
    window.iren.Initialize() # Need this line to actually show the render inside Qt
    sys.exit(app.exec_())