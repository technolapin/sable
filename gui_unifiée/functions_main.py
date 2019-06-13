import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=sauve_recup_objets
import shelve # Permet de sauvegarder et charger des variables

from numpy import load

from class_Fenetre import Fenetre
from parametres import PREFIX_VAR_ENV


"""
Fonction de validation du fichier demandé
@param fichier : Fichier choisi par l'utilisateur
@param lancer : True pour lancer un traitement, False pour ouvrir un traitement
"""
# TODO : A améliorer !
def validationFichier( fichier, lancer ) :
    if fichier == "" :
        return False
    if lancer and fichier[-4:] != ".tiff" :
        return False
    if not lancer and fichier[-4:] != ".dat" :
        return False
    return True


"""
Fonction de traitement d'image (Appel tout le travail de traitement d'image)
@param fichier : Fichier TIFF choisi par l'utilisateur
"""
def traitementImage( fichier ) :
    fichierExporte = "./exemple_fichier_exportation/exemple.dat"
    return fichierExporte


"""
Importer un fichier exporté par le système de traitement
@param fichier : Fichier d'exportation du traitement
@return False si ça a merdé
"""
def importerTraitement( fichier ) :
    print( "[Info] Importation du traitement : " + fichier )
    try :
        fichierExporté = shelve.open( fichier[0:-4], flag='c' ) # 'c' pour lecture seule
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
            # On les met en variables d'environnement pour que parametres.py puisse les récupérer facilement lorsqu'il est appelé par les autres parties du projet
            os.environ[ PREFIX_VAR_ENV + variable ] = str( fichierExporté[ variable ] )
        except KeyError :
            print( "[Erreur] Le fichier ne contient pas les variables nécéssaires !" )
            OK = False
    
    # Sauvegarde du répertoire absolu du répertorie du fichier d'exportation
    # Sert à localiser à partir des URL relatives qu'il contient
    os.environ[ PREFIX_VAR_ENV + "REPERTOIRE" ] = os.path.dirname(os.path.abspath( fichier ))
    
    fichierExporté.close()
    return OK


"""
Ouvrir fichier Numpy (.npy) pour Graphique 3D
"""
def loadGraphique3D( fichierNumpy ) :
#    return load( fichierNumpy )[30:50]
    return load( fichierNumpy )


"""
Demande à l'utilisateur un fichier pour lancer un traitement ou ouvrir un fichier de traitement
@param lancer : True pour lancer un traitement, False pour ouvrir un traitement
"""
def lancerOuOuvrirTraitement( lancer, application ) :
    fileDialog = QFileDialog() # Crée un objet de type QFileDialog (Fenêtre pour choisir un fichier)
    if lancer : fileDialog.setWindowTitle("Veuillez choisir le fichier TIFF") # Définit le nom de la fenêtre
    else : fileDialog.setWindowTitle("Veuillez choisir le fichier DAT")
    fichierDemande = fileDialog.getOpenFileName()[0] # Permet aussi d'attendre qu'il y ait un fichier demandé
    print( "[Debug] Fichier demandé : " + fichierDemande )
    fileDialog.close() # Fermer la fenêtre
    
    if not validationFichier( fichierDemande, lancer ) : # Si la validation de ce fichier échoue
        if lancer : QMessageBox.about(None, "Information", "Ce fichier est invalide ! Il nous faut un .TIFF !")
        else : QMessageBox.about(None, "Information", "Ce fichier est invalide ! Il nous faut un .DAT !")
    else :
        if lancer :
            fichierExporte = traitementImage( fichierDemande )
            autorisationDeLancer = importerTraitement( fichierExporte )
        else :
            autorisationDeLancer = importerTraitement( fichierDemande )
        
        if autorisationDeLancer :
            # TODO : Passer en param à la GUI le fichier du traitement
            # C'est fait avec les variables d'environnement, et récupéré par parametres.py
            fenetre = Fenetre( loadGraphique3D( os.environ[ PREFIX_VAR_ENV + "URL_GRAPHIQUE_3D" ] ) ) # Crée un objet de type Fenetre
            fenetre.setWindowTitle("Graphique 3D (DÉMONSTRATION)") # Définit le nom de la fenêtre
            fenetre.show() # Affiche la fenêtre
            application.exec_() # Attendre que tout ce qui est en cours soit exécuté
        else :
            QMessageBox.about(None, "Information", "Fichier .DAT inutilisable !")