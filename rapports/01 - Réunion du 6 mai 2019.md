# Réunion du 6 mai 2019

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

### Introduction

Cette première réunion pose les bases de notre projet.

Notre projet est donc un projet d'analyse d'image.
Plus précisémment, il consiste à analyser une image en 4 dimensions (Les 3 dimensions spatiales, et le la dimension temporelle) de mouvement de grains de sable. C'est un besoin des géomécaniciens.
Nous disposons d'une série de séries de coupes. Une coupe est une image en deux dimensions. Chaque série est donc une image en 3 dimensions, et cette série de séries fait une image en 4 dimensions.

On cherche à savoir comment bougent les grains de sable.

Dans un premier temps, on va traiter les images en deux dimensions, puis ajouter la dimension temporelle.

Le projet est séparé en deux parties pouvent être réalisées indépendemments...

### Partie segmentation

Le but de cette partie est d'identifier chaque grain de sable, d'extraire chaque grain.
Le mouvement de chaque grain intègre aussi sa rotation... Mais nous verrons ça bien plus tard. D'abord la trajectoire !

On a une grosse  image, on la découpe en petites parties pour simplifier pour le moment.

### Partie visualisation

L'objectif du projet est de savoir comment chaque grain bouge, il faut donc aussi afficher leur trajectoire dans un espace 3D.

Ca serait bien de pouvoir cliquer sur un grain et d'afficher sa trajectoire. Il faut faire un logiciel intuitif et adapté.

A terme, il faut faire une interface graphique qui intègre l'ensemble du projet.
Créer ce logiciel interactif est déjà un bon objectif.
Faire appel à des librairies ! On n'est pas là pour tout refaire.

### Librairie

Nous disposons de la librairie d'analyse d'images "Pink".

Nous disposons des salles 5207 et 5209 pour avancer notre projet.
