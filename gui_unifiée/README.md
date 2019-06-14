# GUI

## Utilisation
Exécuter `python3 main.py` pour avoir toutes les fonctionnalités.
Cela demandera à l'utilisateur si il veut commencer un traitement, ou en charger un.

Exécuter `python3 class_Fenetre.py` pour avoir l'environnement de démonstration uniquement.
Cela chargera les paramètres de démonstration contenus dans `parametres.py`.

Exécuter une `python3 class_Tab*.py` pour avoir les onglets séparemments.
Cela chargera les paramètres de démonstration contenus dans `parametres.py`.

## Composants
* `class_Graphique3D.py` : Contient l'objet `Graphique3D`, qui hérite de `FigureCanvasQTAgg`. Gère un graphique MatPlotLib avec des courbes pour un environnement Qt.
* `class_MilleFeuille3D` : Contient l'objet `MilleFeuille3D`, qui hérite de `FigureCanvasQTAgg`. Gère un graphique MatPlotLib avec des couches d'images pour un environnement Qt.
* `class_MilleFeuilleIRM` : Contient l'objet `MilleFeuilleIRM`, qui hérite de `FigureCanvasQTAgg`. Gère un graphique MatPlotLib avec 3 images orthogonales pour un environnement Qt.

* `class_TabAffichageCoupes.py` : Contient l'objet `TabAffichageCoupes`, qui hérite de `QGridLayout`. Crée une grille Qt contenant un affichage 2D des coupes dans l'espace 3D.
* `class_TabAide.py` : Contient l'objet `TabAide`, qui hérite de `QGridLayout`. Crée une grille Qt contenant des textes d'aide sur les autres onglets. Ces textes sont dans le répertoire `contenu_aide`.
* `class_TabGraphique3D.py` : Contient l'objet `Tab`, qui hérite de `QGridLayout`. Crée une grille Qt contenant l'objet `Graphique3D` et son interaction.
* `class_TabMilleFeuille3D.py` : Contient l'objet `TabMilleFeuille3D`, qui hérite de `QGridLayout`. Crée une grille Qt contenant l'objet `MilleFeuille3D` et son interaction.
* `class_TabMilleFeuilleIRM.py` : Contient l'objet `TabMilleFeuilleIRM`, qui hérite de `QGridLayout`. Crée une grille Qt contenant l'objet `MilleFeuilleIRM` et son interaction.
* `class_TabVTK.py` : Contient l'objet `TabVTK`, qui hérite de `QGridLayout`. Crée une grille Qt contenant un modèle 3D des coupes et son interaction.

* `class_Fenetre.py.py` : Contient l'objet `Fenetre`, qui hérite de `QTabWidget`. Crée la fenêtre Qt à onglets et crée les onglets avec les objets ci-dessus commençant par `Tab`.

* `class_Parametres.py` : Contient l'objet `Parametres`. Gère les paramètres de l'environnement. Il est passé en paramètres à l'objet `Fenetre`, qui le passe à ses onglets. Cela permet d'avoir des variables et des fonctions associées disponibles à tous les onglets.

* `function_readPGM.py` : Contient la fonction `readPGM()`. Permet de lire les fichiers PGMs pour les objets `Graphique3D`, `MilleFeuille3D` et `MilleFeuilleIRM`.
* `functions_main.py` :  Contient la fonction `lancerOuOuvrirTraitement()`. Lance ou ouvre un traitement, lis les paramètres d'un fichier de sauvegarde, crée un objet `Parametre` et lance l'interface via un objet `Fenetre`.
* `main.py` :  Script principal. Crée une interface simple pour savoir si l'utilisateur veut lancer ou ouvrir un traitement, et exécute `lancerOuOuvrirTraitement()`.

* `parametres_par_defaut.py` : Contient les paramètres par défaut pour un objet `Parametre`, c'est-à-dire de démonstration.
* `parametres_graph3D_pour_demo.py` : Contient le contenu par défaut de `Graphique3D`, c'est-à-dire de démonstration.

* `contenu_aide` : Répertoire contenant les fichiers d'aide utilisés par un objet `TabAide`.
* `exemple_fichier_exportation/exporter.py` : Script indépendant permetant de créer un fichier de sauvegarde d'un traitement. Il est suffisemment documenté pour comprendre ce que contient ce type de fichier.

## Fichier de sauvegarde
Le fichier de sauvegarde, appelé aussi "fichier d'importation", ou "traitement chargé", contient des variables Python, qu'on appelle "paramètres" pour la GUI. Parmis ces variables, il y a notamment les URL des répertoire contenant les fichiers PGM et les fichiers VTK. Il est important de noter que ces URL doivent être relatives au fichier de sauvegarde.