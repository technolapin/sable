# CE QU'ON A FAIT
* On a réuni interface et traitement d'images


* Maylis a amélioré le système d'affichage des coupes 


* On peut visualiser les différentes étapes du traitement et afficher la trajectoire du grain cliqué





# À FAIRE 


* Il serait pas mal d'indiquer où se situent les coupes par rapport aux autres (mais nous n'avons pas le temps

)
* Changer les couleurs de la carte des distances pour l'adapter aux daltoniens, colorblind...
* Donner une couleur qui serait en rapport avec le temps (gradiant de couleur)


* Simplifier les maillages (utiliser decimate (in, réduction, out) qui supprime des triangles) pour accélérer le temps de process (on peut faire avec ou sans perte d'info selon si c'est important ou non)


* Utiliser meshregul pour avoir des grains comportements sphériques (pas très utile vu les grains qu'on a deja (mcubes fait déjà un lissage des grains))


* Mentionner au jury (au jdp) et dans le rapport qu'on peut avoir accès à la vitesse des grains au cours du temps et à leur accélération vu qu'on a leur position (on peut aussi avoir la vitesse moyenne,...). Tout ça est utile pour l'analyse du mouvement des grains. Regarder toutes ces valeurs avant le jdp.

* On peut extraire les grains qui touchent le bord ou examiner les trajectoires pour voir s'il y en a des bizarres (qu'on ne connais pas, etc)
* Virer les grains sur les bords pour avoir des jolies images 3D (utiliser enframe ou frame et geodilate(binaire, marqueur, -1)). Dans geodilate -1 est le nombre d'itération pour dire qu'on le fait à l'infini. Ça va extraire les composantes connexes blanches qui sont marquées par chacun des coins du bord


* Changer le nom de l'onglet VTK et l'onglet visualisation graphique ainsi que le mille feuilles (Visualisation 3D, Trajectoire des grains, Visualisation mille feuilles par ex)


* Dans l'onglet aide ou dans un onglet "À propos"/"Objectifs" remettre en contexte le projet en reprenant ce qu'avait écrit Yukiko dans la page de présentation du projet 





# ON EST EN TRAIN DE 

* Vérifier si les trajectoires des grains que l'on a sont les bonnes en superposant des images générées a partir des résultats aux images 3D générées a partir des coupes originales


* Changer le contenu des onglets d'aide pour y expliquer comment on a obtenu telle ou telle image





# POUR LA PRÉSENTATION 
* On peut pas tout détailler donc aborder de façon globale et valoriser le projet en montrant que ce qu'on a réalisé est important dans son contexte (en quoi ça va aider d'autres personnes que nous pour faire du traitement d'images dans le cadre de notre cursus a l'ESIEE,...) 
* Rafraichir la mémoire du jury en rappelant le contexte tout en restant le plus simple possible (ne pas être trop technique) 
* Ne pas s'interdire de faire une descente technique (c'est important) mais ne pas s'y perdre et dire pourquoi c'est important 


* Identifier et mettre en valeur ce qui est le plus intéressant pour nous dans ce projet (ce qu'on a le plus aimé apprendre/faire dans le projet)

* Avoir une réflexion sur comment on a fonctionné en réu, comment on s'est organisé (répartition des taches, etc)


* Répéter la présentation, se chronometrer