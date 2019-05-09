# Souce : https://stackoverflow.com/questions/52379426/pyqta-matplotlib-how-to-redraw-update-a-3d-surface-plot-in-a-window
# Il faut maintenant comprendre tout ce code.

import sys
from PyQt4.QtCore import * # Python Qt4 bindings for GUI objects
from PyQt4.QtGui import *
from math import * # For fun log()
import numpy as np
from matplotlib.figure import Figure # For Matplotlib Figure Object
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

class ThreeDSurface_GraphWindow(FigureCanvas): #Class for 3D window
    def __init__(self):
        self.fig =plt.figure(figsize=(7,7))
        FigureCanvas.__init__(self, self.fig) #creating FigureCanvas
        self.axes = self.fig.gca(projection='3d')#generates 3D Axes object
        self.axes.hold(False)#clear axes on each run
        self.setWindowTitle("Main") # sets Window title

    def DrawGraph(self, x, y, z):#Fun for Graph plotting
        self.axes.clear()
        self.axes.plot_surface(x, y, z) #plots the 3D surface plot
        self.draw()


class TabConfigWidget(QWidget):# The QWidget in which the 3D window is been embedded
    def __init__(self, parent=None):
        super(TabConfigWidget, self).__init__(parent)
        self.Combo=QComboBox()#ComboBox for change index
        self.Combo.addItems(['Graph1','Graph2'])#add indexes to ComboBox
        self.Combo.currentIndexChanged.connect(self.IndexChanged)#Invokes Fun IndexChanged when current index changes
        self.ThreeDWin = ThreeDSurface_GraphWindow()#creating 3D Window
        MainLayout = QGridLayout()# Layout for Main Tab Widget
        MainLayout.setRowMinimumHeight(0, 5) #setting layout parameters
        MainLayout.setRowMinimumHeight(2, 10)
        MainLayout.setRowMinimumHeight(4, 5)
        MainLayout.addWidget(self.Combo, 1, 1)#add GroupBox to Main layout
        MainLayout.addWidget(self.ThreeDWin,2,1)#add 3D Window to Main layout
        self.setLayout(MainLayout) #sets Main layout
        x=np.linspace(-6,6,30) #X coordinates
        y=np.linspace(-6,6,30) #Y coordinates
        X,Y=np.meshgrid(x,y) #Forming MeshGrid
        Z=self.f(X,Y)
        self.ThreeDWin.DrawGraph(X,Y,Z)#call Fun for Graph plot

    def f(self,x,y):#For Generating Z coordinates
        return np.sin(np.sqrt(x**2+y**2))

    def IndexChanged(self):#Invoked when the ComboBox index changes
        x = np.linspace(np.random.randint(-5,0), np.random.randint(5,10), 40) #X coordinates
        y = np.linspace(np.random.randint(-5,0), np.random.randint(5,10), 40) #Y coordinates


        X, Y = np.meshgrid(x, y) #Forming MeshGrid
        Z = self.f(X, Y)
        self.ThreeDWin.DrawGraph(X, Y, Z) #call Fun for Graph plot

class GSPP(QTabWidget): #This is the Main QTabWidget
    def __init__(self, parent=None):
        super(GSPP, self).__init__(parent)
        self.tab1 = TabConfigWidget()
        self.addTab(self.tab1, "Tab1         ") #adding the QWidget

    def Refresh(self): #Fun to refresh
        return

if __name__ == '__main__':  #The Fun for Main()
    app = QApplication(sys.argv)
    Window = GSPP()
    Window.setWindowTitle("Main")
    qr = Window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    Window.move(qr.topLeft())
    Window.showMaximized()
    app.processEvents()
    sys.exit(app.exec_())