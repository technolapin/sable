# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:54:52 2019

@author: Maylis
"""
        
from tkinter import *
from tkinter import ttk


class Interface(): #Création d'une classe d'objet Interface
    def __init__(self) : #Initialisation d'un objet Interface
        self.fenetre=Tk() #Création d'une fenêtre
        self.syst_onglets=ttk.Notebook(self.fenetre) #Création d'un système d'onglets
        self.syst_onglets.pack() # ... que l'on insère dans la fenêtre
        
        #Paramétrage de l'onglet 1      
        self.onglet1=ttk.Frame(self.fenetre) #Création d'un onglet
        self.onglet1.pack() # ... que l'on insère dans la fenêtre
        self.syst_onglets.add(self.onglet1, text='Aide') # ... dans le système d'onglet
        text = Text(self.onglet1, font=('Cambria',10)) # Création du texte dans onglet 1
        text.insert(INSERT,"Projet E3 : Analyse de mouvements de grains de sable dans une séquence d'images 3D\n")
        text.insert(INSERT,"\nBienvenue dans notre interface d'analyse de mouvements de grains de sable dans une séquence d'images 3D.\n")
        text.insert(INSERT,"\n *Onglet 1* : Aide destinée à comprendre l'intérêt des autres onglets.\n")
        text.insert(INSERT,"\n *Onglet 2* : Visualisation du mouvement global des grains de sable.\n")
        text.insert(INSERT,"\n *Onglet 3* : Visualisation du mouvement d'un unique grain de sable.\n")
        text.pack() # Insertion du texte dans la l'onglet 1
        text.tag_add("Titre", "1.0", "1.100") 
        text.tag_config("Titre", font=('bold')) #Mise de la première ligne sous forme de titre
        
        
        #Paramétrage de l'onglet 2
        self.onglet2=ttk.Frame(self.fenetre) #Création d'un onglet
        self.onglet2.pack() # ... que l'on insère dans la fenêtre
        self.syst_onglets.add(self.onglet2, text='Visu courbes') # ... dans le système d'onglet
        
        ####### INTEGRER CE QU'A FAIT AMAURY mais soucis c'est qu'on a pas fait la même chose
        ## Enfin pas sur le même outil pour les fenêtres donc faut reprendre ça et l'intégrer
        
        
        self.fenetre.mainloop() #Boucle d'exécution de ce qui précède

interface=Interface() #Création d'un objet interface
        


### BROUILLON

#      #  self.Tbl=["Aide", "Visualisation des courbes", "Visualisation grain de sable unique", "hey"]
#       # for i in range (len(self.Tbl)) :
#        #    LabelFrame(self.canvas,text=self.Tbl[i])
#
##Button(o1, text='Quitter', command=jeu.destroy).pack(padx=100, pady=100)
##Button(o2, text='En attente', command=None).pack(padx=100, pady=100)
