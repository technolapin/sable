import os

from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Source : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=sauve_recup_objets
import shelve # Permet de sauvegarder et charger des variables

from class_Parametres import Parametres

from class_Fenetre import Fenetre



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
@return False si ça a merdé, ou si les données ont des incohérences
"""
def importerTraitement( fichier, objParams ) :
    print( "[Info Main] Importation du traitement : " + fichier )
    try :
        cheminSansExtension = os.path.splitext(fichier)[0]
        fichierExporté = shelve.open( cheminSansExtension, flag='c' ) # 'c' pour lecture seule
    except Exception :
        print( "[Erreur] Fichier invalide !" )
        return False
    
    try :
        objParams.NB_IMGS = fichierExporté[ "NB_IMGS" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables NB_IMGS !" )
        return False
    try :
        objParams.INTERVALLE_XY = fichierExporté[ "INTERVALLE_XY" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables INTERVALLE_XY !" )
        return False
    try :
        objParams.INTERVALLE_XZ = fichierExporté[ "INTERVALLE_XZ" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables INTERVALLE_XZ !" )
        return False
    try :
        objParams.INTERVALLE_YZ = fichierExporté[ "INTERVALLE_YZ" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables INTERVALLE_YZ !" )
        return False
    try :
        objParams.URL_PGM = fichierExporté[ "URL_PGM" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables URL_PGM !" )
        return False
    try :
        objParams.URL_VTK = fichierExporté[ "URL_VTK" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables URL_VTK !" )
        return False
    try :
        objParams.URL_GRAPHIQUE_3D = fichierExporté[ "URL_GRAPHIQUE_3D" ]
    except KeyError :
        print( "[Erreur] Le fichier ne contient pas la variables URL_GRAPHIQUE_3D !" )
        return False
    
    
    objParams.contientVariablesImportees = True
    
    # Sauvegarde du répertoire absolu du répertorie du fichier d'exportation
    # Sert à localiser à partir des URL relatives qu'il contient
    objParams.CHEMIN_ABSOLU_FICHIER_IMPORTE = os.path.dirname(fichier)
    
    fichierExporté.close()
    
    return objParams.verifierParams()


"""
Demande à l'utilisateur un fichier pour lancer un traitement ou ouvrir un fichier de traitement
@param lancer : True pour lancer un traitement, False pour ouvrir un traitement
"""
def lancerOuOuvrirTraitement( lancer, application ) :
    fileDialog = QFileDialog() # Crée un objet de type QFileDialog (Fenêtre pour choisir un fichier)
    if lancer : fileDialog.setWindowTitle("Veuillez choisir le fichier à traiter") # Définit le nom de la fenêtre
    else : fileDialog.setWindowTitle("Veuillez choisir le fichier à importer")
    fichierDemande = fileDialog.getOpenFileName()[0] # Permet aussi d'attendre qu'il y ait un fichier demandé
    print( "[Debug] Fichier demandé : " + fichierDemande )
    fileDialog.close() # Fermer la fenêtre
    
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
        fenetre.setWindowTitle("Graphique 3D") # Définit le nom de la fenêtre
        fenetre.show() # Affiche la fenêtre
        application.exec_() # Attendre que tout ce qui est en cours soit exécuté
    else :
        QMessageBox.about(None, "Information", "Fichier inutilisable !")