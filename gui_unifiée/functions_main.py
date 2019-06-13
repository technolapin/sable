import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=sauve_recup_objets
import shelve # Permet de sauvegarder et charger des variables

from class_Parametres import Parametres

from class_Fenetre import Fenetre


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
def importerTraitement( fichier, objParams ) :
    print( "[Info Main] Importation du traitement : " + fichier )
    try :
        fichierExporté = shelve.open( fichier[0:-4], flag='c' ) # 'c' pour lecture seule
    except Exception :
        print( "[Erreur] Fichier invalide !" )
        return False
    
    try :
        objParams.setNB_IMGS( fichierExporté[ "NB_IMGS" ] )
        objParams.setINTERVALLE_XY( fichierExporté[ "INTERVALLE_XY" ] )
        objParams.setINTERVALLE_XZ( fichierExporté[ "INTERVALLE_XZ" ] )
        objParams.setINTERVALLE_YZ( fichierExporté[ "INTERVALLE_YZ" ] )
        objParams.setURL_PGM( fichierExporté[ "URL_PGM" ] )
        objParams.setURL_VTK( fichierExporté[ "URL_VTK" ] )
        objParams.setURL_GRAPHIQUE_3D( fichierExporté[ "URL_GRAPHIQUE_3D" ] )
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas les variables nécéssaires !" )
        return False
    
    # Sauvegarde du répertoire absolu du répertorie du fichier d'exportation
    # Sert à localiser à partir des URL relatives qu'il contient
    objParams.setCHEMIN_ABSOLU_FICHIER_IMPORTE( os.path.dirname(os.path.abspath( fichier )) )
    
    fichierExporté.close()
    return True


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
        creationObjParams = Parametres()
        if lancer :
            fichierExporte = traitementImage( fichierDemande )
            autorisationDeLancer = importerTraitement( fichierExporte, creationObjParams )
        else :
            autorisationDeLancer = importerTraitement( fichierDemande, creationObjParams )
        
        if autorisationDeLancer :
            # TODO : Passer en param à la GUI le fichier du traitement
            # C'est fait avec les variables d'environnement, et récupéré par parametres.py
            fenetre = Fenetre( objParams = creationObjParams ) # Crée un objet de type Fenetre
            fenetre.setWindowTitle("Graphique 3D (DÉMONSTRATION)") # Définit le nom de la fenêtre
            fenetre.show() # Affiche la fenêtre
            application.exec_() # Attendre que tout ce qui est en cours soit exécuté
        else :
            QMessageBox.about(None, "Information", "Fichier .DAT inutilisable !")