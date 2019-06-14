# GUI

## Utilisation
Exécuter `python3 main.py` pour avoir toutes les fonctionnalités.
Cela demandera à l'utilisateur si il veut commencer un traitement, ou en charger un.

Exécuter `python3 class_Fenetre.py` pour avoir l'environnement de démonstration uniquement.
Cela chargera les paramètres de démonstration !

Exécuter une `python3 class_Tab*.py` pour avoir les onglets séparemments.
Cela chargera les paramètres de démonstration !

## Paramètres de démonstrations
Les paramètres de démonstration sont contenus dans `parametres.py` et `parametres_graph3D_pour_demo.py`. Ne pas modifier ce dernier fichier !

Il est important de noter que `parametres.py` récupère les paramètre d'un traitement ouvert ou effectué par l'utilisateur, et remplace alors les paramètres par défaut (i.e. de démonstration).

## Composants

* `class_Graphique3D.py` : Contient l'objet `Graphique3D`, qui hérite de `FigureCanvasQTAgg`. Gère un graphique MatPlotLib avec des courbes pour un environnement Qt.
* `class_MilleFeuille3D` : Contient l'objet `MilleFeuille3D`, qui hérite de `FigureCanvasQTAgg`. Gère un graphique MatPlotLib avec des couches d'images pour un environnement Qt.
* `class_MilleFeuilleIRM` : Contient l'objet `MilleFeuilleIRM`, qui hérite de `FigureCanvasQTAgg`. Gère un graphique MatPlotLib avec 3 images orthogonales pour un environnement Qt.

* `class_TabAffichageCoupes` : Contient l'objet `TabAffichageCoupes`, qui hérite de `QGridLayout`. Crée une grille Qt contenant un affichage 2D des coupes dans l'espace 3D.
* `class_TabAide` : Contient l'objet `TabAide`, qui hérite de `QGridLayout`. Crée une grille Qt contenant des textes d'aide sur les autres onglets.
* `class_TabGraphique3D` : Contient l'objet `Tab`, qui hérite de `QGridLayout`. Crée une grille Qt contenant l'objet `Graphique3D` et son interaction.
* `class_TabMilleFeuille3D` : Contient l'objet `TabMilleFeuille3D`, qui hérite de `QGridLayout`. Crée une grille Qt contenant l'objet `MilleFeuille3D` et son interaction.
* `class_TabMilleFeuilleIRM` : Contient l'objet `TabMilleFeuilleIRM`, qui hérite de `QGridLayout`. Crée une grille Qt contenant l'objet `MilleFeuilleIRM` et son interaction.
* `class_TabVTK` : Contient l'objet `TabVTK`, qui hérite de `QGridLayout`. Crée une grille Qt contenant un modèle 3D des coupes et son interaction.

* `class_Fenetre.py` : Contient l'objet `Fenetre`, qui hérite de `QTabWidget`. Crée la fenêtre Qt à onglets et crée les onglets avec les objets ci-dessus commençant par `Tab`.

* `class_Parametres` : Contient l'objet `Parametres`. Gère les paramètres de l'environnement. Il est passé en paramètres à l'objet `Fenetre`, qui le passe à ses onglets. Cela permet d'avoir des variables et des fonctions associées disponibles à tous les onglets.

* `function_readPGM` : Contient la fonction `readPGM()`. Permet de lire les fichiers PGMs pour les objets `Graphique3D`, `MilleFeuille3D` et `MilleFeuilleIRM`.
* `functions_main` :  Contient la fonction `lancerOuOuvrirTraitement()`. Lance ou ouvre un traitement, lis les paramètres, crée un objet `Paramètre` et lance l'interface via un objet `Fenetre`.
* `main` :  Script principal. Crée une interface simple pour savoir si l'utilisateur veut lancer ou ouvrir un traitement, et exécute `lancerOuOuvrirTraitement()`.