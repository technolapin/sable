# Aide rapide avec GIT

## A faire une seule fois

Télécharger GIT. Une fois installé, pour Windows, aller dans le répertoire voulu, faire un clique droit et sélectionner `Git Bash here`.

Cloner le dépôt : `git clone https://github.com/technolapin/sable.git`.

Enregistrer son adresse mail pour les commits : `git config user.email "user@domain.tld"`.
Bien mettre l'adresse associée à son compte GitHub pour que les commits soient associés à ce compte.

## Mettre à jour

Pour mettre à jour depuis le dépôt distant : `git pull`.

A faire de temps en temps. Cela permet de récupérer toutes les modifications des collaborateurs.

## Enoyer ses modifications

Ajouter le fichier : `git add leFichier.ext`.
On peut ajouter plusieurs fichiers, ou des répertoires.

Commit ses modifications : `git commit -m "Qu'avez vous fait ?"`.
On peut ne faire que `git commit`. A ce moment là, votre éditeur de texte favoris s'ouvrira pour vous demander le message. La première ligne de ce message sera le titre sur Github.

Envoyer sur le serveur ses modifications : `git push`.
C'est comme `git pull`, mais dans l'autre sens.
