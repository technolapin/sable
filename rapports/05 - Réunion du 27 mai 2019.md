# Réunion du 27 mai 2019

## Participants

Encadrants du projet :
* J. COUSTY : `jean.cousty@esiee.fr`
* Y. KENMOCHI : `yukiko.kenmochi@esiee.fr`

Participants du projet :
* Clément CHOMICKI : `clement.chomicki@edu.esiee.fr`
* Amaury BARUZY : `amaury.baruzy@edu.esiee.fr`
* Alexandre LEBLON : `alexandre.leblon@edu.esiee.fr`
* Maylis MONTANI : `maylis.montani@edu.esiee.fr`
* Barbara PARE  : `barbara.pare@edu.esiee.fr`

## Compte-rendu de la réunion

### Partie traitement d'image 

* Clément a expliqué que nous étions passé dans l'analyse 3D du mouvement des grains de sable. Nous avons testé l'affichage à l'aide de l'utilitaire "ParaView". M. Cousty nous dit que c'est un bon utilitaire.
* Barbara a généré les images en 3D et les différentes coupes dans les axes (x,y), (x,z) et (y,z).
* Clément a montré le gif des coupes avec les couleurs aux profs. Il y a des petites erreurs qui donnent des trous dans l'image, mais en moyenne il y a peu d'erreurs dans ce qu'il a fait.
* Clément est passé aux distances euclidiennes et a utilisé un paramètre de connexité.
* Pour visualiser les résultats, M. Cousty nous recommande d'utiliser une commande "border" qui prend les bords de l'image segmentée, puis "surimp" (?) qui superpose les bords à l'image d'origine. Cela permet de voir à quoi correspond la coupe.
* M. Cousty veut que nous regardions la séparattion des grains en 2D+T (c'est à dire regarder la même coupe à des temps différents et les empiler). Nous devrions obtenir des genre de cylindres pour les grains qui ne bougent pas dans l'image, et sinon des genre de "rubans" pouvant s'épaissir ou diminuer dans l'image obtenue en 2D+T. REMARQUE : Ceci est une étape intermédiaire avant d'attaquer le 3D+T, car jusque là c'était relativement facile de passer du 2D au 3D car les outils de la librairie "Pink" fonctionnait de la même manière, mais quand nous allons passer en 4D, cela risque d'engendrer de nombreux bugs et nous devrons batailler avec python pour réussir à obtenir ce que nous voulons. Cette étape risque de prendre beaucoup de temps.
* Clément a évoqué le diagramme de Verneuil, et M. Cousty nous a dit que c'était strictement équivalent à ce que nous avions fait (Watershade avec des distances discrètes (?)). Cependant, Clément n'arrive pas à faire fonctionner l'utilitaire.
* Pour visualiser un grain, il faut faire "select comp" (?), cela permet d'avoir un grain ou plusieurs et de le visualiser en 3D avec l'outil.
* Après avoir visualisé ce que l'on souhaite, on pourra peut être diminuer le nombre de triangles affichés pour avoir plus de visibilité et s'autoriser à lisser un peu la forme.


### Partie interface graphique 

* Maylis a intégré les différents outils dont on parlait à la dernière réunion dans l'interface. M. Cousty approuve l'interface à onglets mais suggère d'ajouter un menu de séléction des datas que l'on souhaite utiliser, et tous les codes d'analyse fonctionnels que Clément et Barbara ont produit pour qu'on puisse y accéder directement.
* Pour le défilement des images dans la visualisation en mille-feuille d'Amaury, il faudrait plutôt utiliser les images en niveau de gris, car les couleurs, c'est pas fou.
* Nous devons chercher comme intégrer dans PyQt une autre interface graphique de visualisation 3D (même si c'est pas franchement propre) à l'intérieur d'une Frame par exemple.
* Pour la prochaine fois, il faut vraiment qu'on puisse visualiser en 3D depuis l'interface.
* Amaury se bat avec PyQt et vtk pour avoir l'affichage graphique avec "ParaView".

### Remarque

* M. Cousty ne nous a pas envoyé le code qu'il devait nous envoyer la semaine dernière mais ne semble pas vouloir nous l'envoyer finalement.
* Sur les deux prochaines semaines, M Cousty ne sera pas là, il n'y aura que Mme Kenmochi.
* Pour modifier une librairie de "Pink", M. Cousty nous recommande de recopier le code dans un fichier séparé, de modifier ce que l'on souhaite et de l'appeler sous un autre nom.
