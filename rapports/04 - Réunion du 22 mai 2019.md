# Réunion du 22 mai 2019

## Participants

Encadrants du projet :
* J. COUSTY : `jean.cousty@esiee.fr`

Participants du projet :
* Clément CHOMICKI : `clement.chomicki@edu.esiee.fr`
* Amaury BARUZY : `amaury.baruzy@edu.esiee.fr`
* Alexandre LEBLON : `alexandre.leblon@edu.esiee.fr`
* Maylis MONTANI : `maylis.montani@edu.esiee.fr`
* Barbara PARE  : `barbara.pare@edu.esiee.fr`

## Compte-rendu de la réunion

### Partie traitement d'image

##### Clément
* Clément n'a pas réussi à utiliser la distance euclidienne pour l'intégrer à son programme. Les distances euclidiennes génèrent des erreurs énormes là où les distances discrètes permettent de faire ce qu'il souhaite plus facilement et plus efficacement.
* M. Couosty n'est pas convaincu par les distances discrètes et souhaite que l'on travaille sur les distances euclidiennes, comme il nous l'avait demandé précedemment. Il pense que cela nous posera des problèmes dans l'analyse des grains de sable en 3 dimensions. M. Cousty nous recommande d'avoir les distances euclidiennes sous la main et nous envoie son code afin qu'on puisse comparer nos résultats aux siens et qu'on essaie de l'intégrer malgré tout.
* Clément utilise une boucle while sous Python pour fusionner les formes trop proches par rapport à leur taille pour être des grains différents. Il est entrain de réimplémenter ce code en C pour le rendre plus rapide, car son programme fonctionne déjà bien mais reste un peu lent. 
* M. Cousty n'y voit pas d'objections et pense que c'est bien qu'on continue sur cette voie.
* Cependant, M. Cousty pense que nous devrions dés à présent nous attaquer aux images 3D, car l'analyse des images 2D n'était là que pour se faire la main sur le problème. Cependant, il souhaite que nous continuons à travailler sur les images 2D jusqu'à l'obtention d'un résultat. Techniquement, ce que nous avons implémenté avec la librairie 'Pink' devrait s'étendre au problème en 3D. Il nous a parlé de deux type d'images 3D que nous devrons générer : 
	* Volume 3D à un temps donné
	* Coupe 2D au cours du temps généré comme  un volume 3D
* M. Cousty est de manière générale convaincu que la méthodologie classique est bien comprise et mise en oeuvre. Nous devons maintenant produire des images lisibles par les opérateurs de la librairie 'Pink' pour voir s'il y a une chance que cela fonctionne en 3D.


#### Barbara
* Barbara voulait faire la correspondance entre les différentes couches de nos images après l'analyse individuelles des coupes 2D. 
* M. Cousty ne veut pas qu'on fasse le lien entre les images 2D, il veut qu'on utilise directement les images en 3D et qu'on étende notre méthode de séparation des grains de sable en 3D. En effet, le problème de séparation de grain de sable se retrouvera en 3D, car les grains se touchent au milieu de nos couches. Ce sera plus rapide et plus efficace de travailler directement en 3D puis 4D.
* Une fois qu'on aura une segmentation, il faudra utiliser les outils '3Dview' ou '3Dsegment' pour sélectionner un grain à un moment donné et vérifier qu'il a bien une forme de 'ballon'.


### Partie interface / Représentation

* Nos devrons utiliser l'ensemble de voxels pour générer une représentation de la surface des grains de sable (surface renderig (?)). L'outil '3Dview' prendra les images pgm en niveau de gris et d'en extraire le format 3D puis l'affichage vtk. 
* Amaury a fait un millefeuille de l'affichage des couches. 
* Visualisation image 3D puis 4D : M. Cousty dit que c'est bien mais qu'il faudrait pousser plus que ça et faire un rendu de coupe dans les 3 dimensions, suivant les axes (x,y), (y,z) et (z,x). Il existe un outil de la librairie 'Pink' qui permet d'afficher les trois coupes simultanément et il veut qu'on y ajoute un curseur suivant les coupes pour voir bouger. 
* Rendu des grains de sable en 3D : M. Cousty explique qu'il faut voir les images qu'on a comme des petits cubes en 3D qui composent l'image 3d mais contenu dans les coupes 2D. Dans la librairie 'Pink', il existe une fonction '2Dto3D' permettant d'attrapper les différentes couches. Il a aussi parlé de 'catpgm' qui permet à partir de plusieurs images 2D de faire une image 3D.
