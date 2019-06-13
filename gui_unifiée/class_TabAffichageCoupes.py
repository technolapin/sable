import os
import sys

#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QScrollBar, QHBoxLayout, QVBoxLayout, QGroupBox,QRadioButton, QPushButton, QProgressBar
import functools
from math import floor

from class_Parametres import Parametres # Ne sert que si est exécuté séparemment


#### Problème parceque dans un autre dossier donc il veut pas ouvrir, depuis
#### le dossier courant, les choses qu'on veut ouvrir sont pas là
#sys.path.append("../extraction")
#from tracking_3D import *


"""
PARAMETRES
"""
IMAGE_AXES = "image_AxesXYZ.png"


"""
Classe TabAffichageCoupes, hérite de la classe QGridLayout, c'est donc une grille
Cette classe représente le contenu d'une fenêtre PyQt
Elle peut donc aussi être utilisée comme un onglet dans une fenêtre
@author Maylis et Alexandre
"""
class TabAffichageCoupes(QGridLayout) :
    """
    Constructeur, crée le contenu de l'onglet
    """
    def __init__(self, objParams, parent=None) :
        super(TabAffichageCoupes, self).__init__(parent) # Appel du constructeur de QGridLayout
        
        self.objParams = objParams
        
        
        vertical_layout=QVBoxLayout()
        
        """
        Barres de Scroll
        """
        # Défilement de la couche X
        self.barreScrollAxeX = QScrollBar()
        self.barreScrollAxeX.setMaximum( self.objParams.nombreImagesPlanYZ() )
        self.barreScrollAxeX.valueChanged.connect( self.changeImages )
        
        # Défilement de la couche Y
        self.barreScrollAxeY = QScrollBar()
        self.barreScrollAxeY.setMaximum( self.objParams.nombreImagesPlanXZ() )
        self.barreScrollAxeY.valueChanged.connect( self.changeImages )
        
        # Défilement de la couche Z
        self.barreScrollAxeZ = QScrollBar()
        self.barreScrollAxeZ.setMaximum( self.objParams.nombreImagesPlanXY() )
        self.barreScrollAxeZ.valueChanged.connect( self.changeImages )
        
        # Défilement temporel
        self.barreScrollTemps = QScrollBar(Qt.Horizontal)
        self.barreScrollTemps.setMaximum( self.objParams.nombreInstantsTemporels() )
        self.barreScrollTemps.valueChanged.connect( self.changeImages )
        
        
        # Ajout des barres de scroll 
        self.addWidget(self.barreScrollTemps, 2, 1)
        self.addWidget(self.barreScrollAxeX, 1, 2)
        self.addWidget(self.barreScrollAxeY, 1, 3)
        self.addWidget(self.barreScrollAxeZ, 1, 4)
        
        
        """
        Images
        """
        # Création d'un contenant pour les images 
        contenant_widget = QWidget()
        contenant_grille = QGridLayout()
        
        self.label_image_xy = QLabel()
        self.label_image_yz = QLabel()
        self.label_image_zx = QLabel()
        
       # print("[Debug TabAffichageCoupes] Image XY : ", self.label_image_xy)
        #print("[Debug TabAffichageCoupes] Image YZ : ", self.label_image_yz)
        #print("[Debug TabAffichageCoupes] Image ZX : ", self.label_image_zx)
        
        self.label_image_xy.mousePressEvent=functools.partial(self.get_pixel, source_object=self.label_image_xy)
        self.label_image_yz.mousePressEvent=functools.partial(self.get_pixel, source_object=self.label_image_yz)
        self.label_image_zx.mousePressEvent=functools.partial(self.get_pixel, source_object=self.label_image_zx)
        
        self.label_image_xy.setFixedSize(240,240)
        self.label_image_yz.setFixedSize(240,500)
        self.label_image_zx.setFixedSize(240,500)

        self.valeur_temps = QLabel("Temps : 0")
        self.valeur_X = QLabel("X : 0")
        self.valeur_Y = QLabel("Y : 0")
        self.valeur_Z = QLabel("Z : 0")
        
        self.changeImages(0)
        
        
        # Ajout des images dans le contenant à images
        contenant_grille.addWidget(self.label_image_xy, 5, 2)
        contenant_grille.addWidget(self.label_image_yz, 2, 3)
        contenant_grille.addWidget(self.label_image_zx, 2, 1)
        contenant_widget.setLayout(contenant_grille)
        
        
        # Textes correspondant aux images
        texte_xy = QLabel("Image (X, Y)")
        texte_yz = QLabel("Image (Y, Z)")
        texte_zx = QLabel("Image (X, Z)")
        
        
        contenant_grille.addWidget(texte_xy, 3, 2)
        contenant_grille.addWidget(texte_yz, 1, 3)
        contenant_grille.addWidget(texte_zx, 1, 1)
        
        self.setColumnStretch(1,2)
        
        # Image des axes
        label_image_axes = QLabel()
        label_image_axes.setPixmap(QPixmap(IMAGE_AXES))
        contenant_grille.addWidget(label_image_axes,2,2)
        if not os.path.isfile( IMAGE_AXES ) : # Si le chemin d'accès à l'image n'existe pas
            print( "[Erreur TabAffichageCoupes] " + IMAGE_AXES + " n'existe pas !" )


        
        
        """
        Positions actuelles X, Y, Z et temps
        """
        horizontal_layout = QHBoxLayout()
        
        horizontal_layout.addWidget(self.valeur_temps)
        horizontal_layout.addWidget(self.valeur_X)
        horizontal_layout.addWidget(self.valeur_Y)
        horizontal_layout.addWidget(self.valeur_Z)

        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(contenant_widget,stretch=2)
        
        self.addLayout(vertical_layout,1,1)
        
        
        
        
        """
        RadioButton pour choisir le traitement à afficher
        """
        group_box1=QGroupBox("Images utilisées")
        
        self.bouton1=QRadioButton("Originales sans contours")
        self.bouton2=QRadioButton("Originales contours blancs")
        self.bouton3=QRadioButton("Originales contours colorés")
        self.bouton4=QRadioButton("Seuillées")
        self.bouton5=QRadioButton("Carte de distance")
        
        self.bouton2.setChecked(True)
        
        vl_boutons1=QVBoxLayout()
        vl_boutons1.addWidget(self.bouton1)
        vl_boutons1.addWidget(self.bouton2)
        vl_boutons1.addWidget(self.bouton3)
        vl_boutons1.addWidget(self.bouton4)
        vl_boutons1.addWidget(self.bouton5)
        
        group_box1.setLayout(vl_boutons1)
        
        contenant=QVBoxLayout()
        contenant.addWidget(group_box1)
        
        self.addLayout(contenant,1,5)
 
        """
        Bouton pour charger l'image et barre de chargement
        """
        bouton_chargement=QPushButton("Modification des images")
        bouton_chargement.clicked.connect(self.charger_images)
        ########## LANCER LE TRAITEMENT A L'AIDE D'UNE FONCTION
        contenant.addWidget(bouton_chargement)
        contenant.addSpacing(50)


#        self.progress = QProgressBar()
#        self.progress.setMaximum(100)
#        
#        contenant.addWidget(self.progress)
        
        
        
        
        """
        Informations sur le grain cliqué et renvoi vers la fenêtre de trajectoire
        """
        ## Création du layout vertical
        ## Création du bouton pour passer à la fenêtre suivante
        bouton_fen_traj = QPushButton("Afficher trajectoire")
        
        ## Création du cadre qui contient les informatins du grain cliqué        
        group_infos=QGroupBox("Informations sur le grain cliqué")
        vl_grain=QVBoxLayout()
        
        self.label_grain_X=QLabel("X : ")
        self.label_grain_Y=QLabel("Y : ")
        self.label_grain_Z=QLabel("Z : ")
        self.label_grain_Temps=QLabel("Temps : ")
        self.label_grain_Ref=QLabel("Référence : ")
        
        vl_grain.addWidget(self.label_grain_X)
        vl_grain.addWidget(self.label_grain_Y)
        vl_grain.addWidget(self.label_grain_Z)
        vl_grain.addWidget(self.label_grain_Temps)
        vl_grain.addWidget(self.label_grain_Ref)
        
        group_infos.setLayout(vl_grain)
        
        ## Ajout dans le layout vertical
        contenant.addWidget(group_infos)
        contenant.addWidget(bouton_fen_traj)
        
        
        
        
        # Ajouter un bouton qui envoie la référence du grain à la fenêtre 
        # d'Amaury pour la trajectoire.
        # Ajouter les labels pour afficher la coordonnée et la référence du 
        # grain qu'on a cliqué.
        
    
    
    def charger_images(self):
        #### LANCER LE CODE DE CLEMENT ET BARBARA
        if (self.bouton1.isChecked()):
            print("Prendre l'image originale sans contours")
        elif (self.bouton2.isChecked()):
            print("Prendre l'image originale avec contours blancs")
        elif (self.bouton3.isChecked()):
            print("Prendre l'image originale avec contours colorés")
        elif (self.bouton4.isChecked()):
            print("Prendre l'image seuillée")
        elif (self.bouton5.isChecked()):
            print("Prendre l'image de carte de distance")
        
        
        
        
       # self.progress.setValue(self.progress.value()+1)
        
        # Lancer les traitements qu'on demande 
        # Faire avancer la barre de progression en fonction de l'avancement
        # Récupérer les URL des résultats créés
        # Changer l'affichage des coupes depuis le lien
    
    
    
    """
    Obtenir la position du clic
    """
    def get_pixel(self, event, source_object=None):
        if (source_object==self.label_image_xy):
            x=floor(event.pos().x()/3)
            y=floor(event.pos().y()/3)
            z=self.barreScrollAxeZ.value()   
        elif (source_object==self.label_image_yz):
            y=floor(event.pos().x()/3)
            z=floor(event.pos().y()/2)
            x=self.barreScrollAxeX.value()
        elif (source_object==self.label_image_zx):
            x=floor(event.pos().x()/3)
            z=floor(event.pos().y()/2)
            y=self.barreScrollAxeY.value()
            
        temps=self.barreScrollTemps.value()
        
        
        ####### Appeler retrouver grain de Barbara
  #      if (traitement_barbara==null):
   #         reference="Cliquez sur un grain !"
    #    else
        reference="référence coucou" ## Traitement de Barbara
        
        
        
        self.label_grain_X.setText("X : " + str(x))
        self.label_grain_Y.setText("Y : " + str(y))
        self.label_grain_Z.setText("Z : " + str(z))
        self.label_grain_Temps.setText("Temps : " + str(temps))
        self.label_grain_Ref.setText("Référence : " + str(reference))
        
        # rapports : x=80   y=80    z=250
        #    image xy :   240 x 240      Diviser par 3  ; Diviser par 3
        #    image yz :   240 x 500      Diviser par 3  ; Diviser par 2
        #    image xz :   240 x 500      Diviser par 3  ; Diviser par 2   
        
        
        #print("x=",x,"   y=",y, "   z=",z,"   temps=",temps)
        # TODO : Appeler le traitement de Barbara pour sélectionner le grain en 3D
    
    """
    Gère l'affichage et son actualisatin
    """    
    def changeImages(self, value) :
        #print ( "[Debug TabAffichageCoupes] Temps : " + str(self.barreScrollTemps.value()) +
         #                                    ", X : " + str(self.barreScrollAxeX.value()) +
          #                                   ", Y : " + str(self.barreScrollAxeY.value()) +
           #                                  ", Z : " + str(self.barreScrollAxeZ.value()) )
        
        # Image plan (X, Y)
        image_xy = self.objParams.genererURLdesPGM3D( 'XY', self.barreScrollTemps.value(), self.barreScrollAxeZ.value() )
        if os.path.isfile( image_xy ) : # Si le chemin d'accès à l'image existe
            width=self.label_image_xy.width()
            height=self.label_image_xy.height()
            self.label_image_xy.setPixmap(QPixmap(image_xy).scaled(width,height,Qt.KeepAspectRatio))
        else :
            print( "[Erreur TabAffichageCoupes] " + image_xy + " n'existe pas !" )

        # Image plan (Y, Z)
        image_yz = self.objParams.genererURLdesPGM3D( 'YZ', self.barreScrollTemps.value(), self.barreScrollAxeX.value() )
        if os.path.isfile( image_yz ) : # Si le chemin d'accès à l'image existe
            width=self.label_image_yz.width()
            height=self.label_image_yz.height()
            self.label_image_yz.setPixmap(QPixmap(image_yz).scaled(width,height,Qt.KeepAspectRatio))
        else :
            print( "[Erreur TabAffichageCoupes] " + image_yz + " n'existe pas !" )
        
        # Image plan (X, Z)
        image_zx = self.objParams.genererURLdesPGM3D( 'XZ', self.barreScrollTemps.value(), self.barreScrollAxeY.value() )
        if os.path.isfile( image_zx ) : # Si le chemin d'accès à l'image existe
            width=self.label_image_zx.width()
            height=self.label_image_zx.height()
            self.label_image_zx.setPixmap(QPixmap(image_zx).scaled(width,height,Qt.KeepAspectRatio))
        else :
            print( "[Erreur TabAffichageCoupes] " + image_zx + " n'existe pas !" )
        
        self.valeur_temps.setText("Temps : " + str(self.barreScrollTemps.value()))
        self.valeur_X.setText("X : " + str(self.barreScrollAxeX.value()))
        self.valeur_Y.setText("Y : " + str(self.barreScrollAxeY.value()))
        self.valeur_Z.setText("Z : " + str(self.barreScrollAxeZ.value()))


"""
Code principal pour démonstration
"""
# Si on est le script principal
# Cela permet de ne pas exécuter ce bloc de codes lorsque ce script est importé par un autre
# Source : https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__' :
    application = QApplication(sys.argv) # Crée un objet de type QApplication (Doit être fait avant la fenêtre)
    fenetre = QWidget() # Crée un objet de type QWidget
    fenetre.setWindowTitle("MODE DÉMONSTRATION") # Définit le nom de la fenêtre
    fenetre.setLayout( TabAffichageCoupes( Parametres() ) )
    fenetre.show() # Affiche la fenêtre
    application.exec_() # Attendre que tout ce qui est en cours soit exécuté
