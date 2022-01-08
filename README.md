# Projet P4 : Application de gestion d'un tournoi d'échecs

### Présentation du script

L'application permet de gérer un tournoi d'échecs ainsi qu'une base de données des joueurs et des tournois.

Les différents scripts utilisés par l'application sont répartis en Modèles, Vues et Contrôleurs.

Le contrôleur principal(controller) s'appuie sur un contrôleur secondeur pour la gestion des données (datamanager)
      
### Création et activation d'un environnement virtuel (procédure sous linux)

Se placer dans le répertoire de travail (existant ou à créer).  
  
Créer un clone du repository au moyen de la commande `git clone https://github.com/Olrio/P4.git`  

Se placer dans le répertoire P4

Créer un environnement virtuel au moyen de la commande : `python -m venv env` 

Activer cet environnement virtuel  avec : `source env/bin/activate`    

Y installer les modules nécessaires à partir du fichier *requirements.txt* : `pip install -r requirements.txt` 

Lancer l'exécution du programme *chess.py* au moyen de la commande : `python chess.py`  

### Principales fonctionnalités de l'application

Lorsque le programme est lancé, l'utilisateur peut choisir entre trois menus.
- Menu Tournoi : Pour créer, charger, supprimer, modifier ou gérer un tournoi
- Menu joueur : Pour créer, charger, supprimer ou éditer un joueur.
- Menu rapports : Pour accéder aux différents rapports d'édition.

La gestion d'un tournoi est accessible via le menu Tournoi ou le menu Joueur (après sélection d'un tournoi).

###Base de données :

Toutes les informations liées aux joueurs et aux tournois sont enregistrées dans une base de données (fichier *data/db.json*)

La base de données, si elle existe, est chargée au lancement du programme.  
Sinon, elle sera créée dans le répertoire *data* dont la présence est donc nécessaire.

Toutes les modifications apportées aux tournois ou aux joueurs sont enregistrées automatiquement dans la base de données. 


### Vérification de la conformité PEP 8

Le fichier *requirements.txt* a permis d'installer le module *flake8-html*.

Celui-ci permet de générer un rapport html qui recense les erreurs de conformité du code par rapport aux directives de la PEP 8.

Pour lancer le module *flak8-html* : utiliser la ligne de commande suivante :

`flake8 --format=html --htmldir=flake-report controller/controller.py controller/datamanager.py  models/crud.py models/data.py models/match.py models/menu.py models/player.py models/round.py models/tournament.py view/view.py chess.py`

Cela permet de vérifier l'ensemble des fichiers constituant l'application.

NOTE : Ce dépôt comprend les dernières versions du projet P4.
Les précédentes peuvent être consultées dans le dépôt : https://github.com/Olrio/OR_OC_ProjectsDAP
