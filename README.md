# OR_OC_ProjectsDAP

## Projet P4 : Application de gestion d'un tournoi d'échecs

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
