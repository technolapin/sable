import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_Fenetre import Fenetre
from parametres_pour_demo import grapheDeDemonstration


"""
Fonction de validation du fichier demandé
@param fichier : Fichier choisi par l'utilisateur
@param lancer : True pour lancer un traitement, False pour ouvrir un traitement
"""
# TODO : A améliorer !
def validationFichier( fichier, lancer ) :
    if fichier == "" :
        return False
    return True


"""
Fonction de traitement d'image (Appel tout le travail de traitement d'image)
@param fichier : Fichier choisi par l'utilisateur
"""
def traitementImage( fichier ) :
    return


"""
Demande à l'utilisateur un fichier pour lancer un traitement ou ouvrir un fichier de traitement
@param lancer : True pour lancer un traitement, False pour ouvrir un traitement
"""
def lancerOuOuvrirTraitement( lancer ) :
    fileDialog = QFileDialog() # Crée un objet de type QFileDialog (Fenêtre pour choisir un fichier)
    if lancer : fileDialog.setWindowTitle("Veuillez choisir le fichier TIFF") # Définit le nom de la fenêtre
    else : fileDialog.setWindowTitle("Veuillez choisir le fichier")
    fichierDemande = fileDialog.getOpenFileName()[0] # Permet aussi d'attendre qu'il y ait un fichier demandé
    print( "[Debug] Fichier demandé : " + fichierDemande )
    fileDialog.close() # Fermer la fenêtre
    
    if not validationFichier( fichierDemande, lancer ) : # Si la validation de ce fichier échoue
        QMessageBox.about(None, "Information", "Ce fichier est invalide !")
    else :
        traitementImage( fichierDemande )
        
        fenetre = Fenetre( grapheDeDemonstration ) # Crée un objet de type Fenetre
        fenetre.setWindowTitle("Graphique 3D (DÉMONSTRATION)") # Définit le nom de la fenêtre
        fenetre.show() # Affiche la fenêtre
        application.exec_() # Attendre que tout ce qui est en cours soit exécuté


"""
Code principal
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
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
        msgBox.setText("Voulez-vous ouvrir un traitement déjà effectué ?")
        msgBox.setWindowTitle("Information")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msgBox.exec()
        
        if returnValue == QMessageBox.Yes :
            print( "[Debug] L'utilisateur veut ouvrir un traitement déjà effectué." )
            lancerOuOuvrirTraitement( False )
        
        else :
            QMessageBox.about(None, "Information", "Au revoir !")