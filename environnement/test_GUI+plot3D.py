# Source : https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies

import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt


import numpy as np

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure(figsize=(15,15))

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        
        
        
        theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
        z = np.linspace(-2, 2, 100)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        
        
        """
        Pour chaque grains de sable :
        x = [ x, x, x, x ]
        y = [ y, y, y, y ]
        z = [ z, z, z, z ]
              =========> t
        Chaque indice des listes est un instant t
        """
        
        """
        GENERATION D'UNE COURBE EN 3D
        """
        
        ax = self.figure.gca(projection='3d')
        
        
        # b = blue
        # o = mettre des ronds
        # - = lier ces ronds
        ax.plot(x, y, z, 'bo-', label='Courbe 1')
        ax.plot(z, x, y, 'ro-', label='Courbe 2')
        ax.plot(y, z, x, 'go-', label='Courbe 3')
        


        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())