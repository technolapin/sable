import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from class_Fenetre import Fenetre

# Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=sauve_recup_objets
import shelve # Permet de sauvegarder et charger des variables

from numpy import load


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
@param fichier : Fichier TIFF choisi par l'utilisateur
"""
def traitementImage( fichier ) :
    fichierExporte = "./exemple_fichier_exportation/exemple"
    return fichierExporte


"""
Importer un fichier exporté par le système de traitement
@param fichier : Fichier d'exportation du traitement
@return False si ça a merdé
"""
def importerTraitement( fichier ) :
    try :
        fichierExporté = shelve.open( fichier[0:-4] )
    except Exception :
        print( "[Erreur] Fichier invalide !" )
        return False
    
    variablesAImporter = [ "NB_IMGS",
                           "INTERVALLE_XY",
                           "INTERVALLE_XZ",
                           "INTERVALLE_YZ",
                           "URL_PGM",
                           "URL_VTK",
                           "URL_GRAPHIQUE_3D" ]
    
    OK = True
    for variable in variablesAImporter :
        try :
            temp = str( fichierExporté[ variable ] )
            print(temp)
            os.environ[variable] = temp
        except KeyError :
            print( "[Erreur] Le fichier ne contient pas les variables nécéssaires !" )
            OK = False
    
    fichierExporté.close()
    return OK


"""
Ouvrir fichier Numpy (.npy) pour Graphique 3D
"""
def loadGraphique3D( fichierNumpy ) :
    return load( fichierNumpy )[30:50]


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
        if lancer :
            fichierExporte = traitementImage( fichierDemande )
            autorisationDeLancer = importerTraitement( fichierExporte )
        else :
            autorisationDeLancer = importerTraitement( fichierDemande )
        
        if autorisationDeLancer :
            # TODO : Passer en param à la GUI le fichier du traitement
            fenetre = Fenetre( loadGraphique3D( "../extraction/tracking_3D/resultats.npy" ) ) # Crée un objet de type Fenetre
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
        msgBox.setText("Voulez-vous ouvrir un traitement déjà effectué ? (Ouvrir un fichier DAT)")
        msgBox.setWindowTitle("Information")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msgBox.exec()
        
        if returnValue == QMessageBox.Yes :
            print( "[Debug] L'utilisateur veut ouvrir un traitement déjà effectué." )
            lancerOuOuvrirTraitement( False )
        
        else :
            QMessageBox.about(None, "Information", "Au revoir !")