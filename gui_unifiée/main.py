import sys

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMessageBox

import platform

from functions_main import lancerOuOuvrirTraitement


"""
Code principal
@author Amaury
"""
application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)

msgBox = QMessageBox()
msgBox.setText("Voulez-vous lancer un nouveau traitement ?")
msgBox.setWindowTitle("Information")
msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
returnValue = msgBox.exec()

if returnValue == QMessageBox.Yes :
    print( "[Info Main] L'utilisateur veut lancer un nouveau traitement." )
    if platform.system() != "Linux" :
        print( "[Info Main] Un système Unix est nécéssaire pour lancer un traitement." )
        QMessageBox.about(None, "Information", "Vous devez exécuter ce logiciel sur un système Linux pour pouvoir réaliser un traitement !\nEn effet, notre système de traitement est compilé uniquement pour cette plateforme.")
    else :
        lancerOuOuvrirTraitement( True, application )
    
else :
    print( "[Info Main] L'utilisateur ne veut pas lancer un nouveau traitement" )
    msgBox = QMessageBox()
    msgBox.setText("Voulez-vous ouvrir un traitement déjà effectué ?")
    msgBox.setWindowTitle("Information")
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    returnValue = msgBox.exec()
    
    if returnValue == QMessageBox.Yes :
        print( "[Info Main] L'utilisateur veut ouvrir un traitement déjà effectué." )
        lancerOuOuvrirTraitement( False, application )
    
    else :
        print( "[Info Main] L'utilisateur ne veut pas ouvrir un traitement déjà effectué." )
        QMessageBox.about(None, "Information", "Au revoir !")