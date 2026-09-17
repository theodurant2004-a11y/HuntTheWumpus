# Projet par Durant Théo et Dellisse Augustin
# Hunt the Wumpus

Adaptation web du jeu classique *Hunt the Wumpus*, développée en Python avec le framework **Flask**, dans le cadre d'un projet de groupe scolaire.

## Description

Le joueur explore un réseau de salles à la recherche du Wumpus, une créature qui se cache quelque part dans la grotte, tout en évitant les pièges (fosses, chauves-souris) disséminés sur le parcours. Le but est de le localiser et de l'abattre à l'aide d'une flèche avant qu'il ne vous surprenne.

## Fonctionnalités

- Système d'authentification (inscription / connexion des joueurs)
- Moteur de jeu avec déplacement dans la grotte et tir de flèches sur le Wumpus
- Écran d'options pour configurer une partie
- Interface web avec templates HTML/CSS dédiés
- Sauvegarde des données via une base de données SQL

## Technologies utilisées

- **Python** / **Flask** (routes, logique serveur)
- **HTML / CSS** (templates Jinja2)
- **SQL** pour la persistance des données (schéma fourni dans `db.sql`)
- Déploiement via WSGI (`py15.wsgi`)

## Installation et lancement

```bash
# Cloner le repo
git clone https://github.com/theodurant2004-a11y/HuntTheWumpus.git
cd HuntTheWumpus

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
# Créer un fichier .env à la racine (voir les variables attendues dans le code)

# Importer le schéma de base de données
# (adapter selon le moteur SQL utilisé, via db.sql)

# Lancer l'application
flask run
```

## Structure du projet

```
HuntTheWumpus/
├── routes/          # Logique serveur (authentification, jeu)
├── templates/        # Pages HTML (Jinja2)
├── static/            # Fichiers statiques (CSS, images...)
├── db.sql              # Schéma de la base de données
├── requirements.txt   # Dépendances Python
└── py15.wsgi            # Fichier de déploiement WSGI
```

## Auteurs

Projet réalisé dans le cadre d'un travail de groupe scolaire.
