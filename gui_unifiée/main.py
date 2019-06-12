import sys

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog

from functions_main import lancerOuOuvrirTraitement


"""
Code principal
"""
application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)

msgBox = QMessageBox()
msgBox.setText("Voulez-vous lancer un nouveau traitement ?")
msgBox.setWindowTitle("Information")
msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
returnValue = msgBox.exec()

if returnValue == QMessageBox.Yes :
    print( "[Debug] L'utilisateur veut lancer un nouveau traitement." )
    lancerOuOuvrirTraitement( True )
    
else :
    print( "[Debug] L'utilisateur ne veut pas lancer un nouveau traitement" )
    msgBox = QMessageBox()
    msgBox.setText("Voulez-vous ouvrir un traitement déjà effectué ? (Ouvrir un fichier .DAT)")
    msgBox.setWindowTitle("Information")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    returnValue = msgBox.exec()
    
    if returnValue == QMessageBox.Yes :
        print( "[Debug] L'utilisateur veut ouvrir un traitement déjà effectué." )
        lancerOuOuvrirTraitement( False, application )
    
    else :
        print( "[Debug] L'utilisateur ne veut pas ouvrir un traitement déjà effectué." )
        QMessageBox.about(None, "Information", "Au revoir !")