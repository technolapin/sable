import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_Fenetre import Fenetre
from parametres_pour_demo import grapheDeDemonstration


"""
Fonction de validation du fichier demandé
"""
# TODO : A améliorer !
def validationFichier( fichier ) :
    if fichier == "" :
        return False
    return True


"""
Fonction de traitement d'image (Appel tout le travail de traitement d'image)
"""
def traitementImage( fichier ) :
    return


"""
Code principal
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    
    fileDialog = QFileDialog() # Crée un objet de type QFileDialog (Fenêtre pour choisir un fichier)
    fileDialog.setWindowTitle("Veuillez choisir le fichier TIFF") # Définit le nom de la fenêtre
    fichierDemande = fileDialog.getOpenFileName()[0] # Permet aussi d'attendre qu'il y ait un fichier demandé
    print( u"[Debug] Fichier demandé : " + fichierDemande ) # "u" pour Unicode
    fileDialog.close() # Fermer la fenêtre
    
    if not validationFichier( fichierDemande ) : # Si la validation de ce fichier échoue
        QMessageBox.about(None, "Information", "Ce fichier est invalide !")
    else :
        traitementImage( fichierDemande )
        
        fenetre = Fenetre( grapheDeDemonstration ) # Crée un objet de type Fenetre
        fenetre.setWindowTitle("Graphique 3D (DÉMONSTRATION)") # Définit le nom de la fenêtre
        fenetre.show() # Affiche la fenêtre
        application.exec_() # Attendre que tout ce qui est en cours soit exécuté
