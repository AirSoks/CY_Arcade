# Cy_Arcade - Système de Gestion de Bornes d'Arcade

Projet de programmation réseau L3 Informatique - CY Cergy Paris Université  
**Année universitaire** : 2025-2026

## Description

Cy_Arcade est un système client-serveur TCP permettant de gérer des bornes d'arcade connectées à une base de données PostgreSQL. Le projet implémente un protocole de communication personnalisé pour :
- Authentifier les joueurs via leur carte
- Gérer le solde de jetons
- Lancer et terminer des parties
- Calculer les récompenses
- Afficher les classements
- Recharger les comptes

## Architecture

```
┌─────────────┐         TCP          ┌─────────────┐         SQL          ┌─────────────┐
│   Client    │ ◄──────────────────► │   Serveur   │ ◄──────────────────► │  PostgreSQL │
│   (Java)    │   Protocole custom   │   (Python)  │                      │             │
└─────────────┘                      └─────────────┘                      └─────────────┘
```

### Technologies utilisées
- **Client** : Java (JDK 8+)
- **Serveur** : Python 3.7+
- **Base de données** : PostgreSQL
- **Protocole** : TCP avec messages textuels délimités par `\n`

## Structure du projet

```
Cy_Arcade/
├── README.md
├── .gitignore
├── server/
│   ├── server.conf        # Configuration serveur et BD
│   ├── server.py          # Point d'entrée du serveur
│   ├── protocols.py       # Gestion des protocoles
│   ├── queries.py         # Requêtes base de données
│   ├── utils.py           # Fonctions utilitaires
│   └── server.log         # Logs (généré automatiquement)
├── client/
│   ├── client.conf        # Configuration client
│   ├── ArcadeClient.java  # Client principal
│   ├── SocketConnexion.java   # Gestion socket + logs
│   ├── ClientConfig.java      # Chargement configuration
│   └── client.log         # Logs client (généré automatiquement)
└── doc/
    └── rapport.pdf        # Rapport de projet
```

## Configuration

### Serveur (`server/server.conf`)

```ini
[SERVER]
HOST = 0.0.0.0
PORT = 50001
TIMEOUT = 30
MAX_COMMANDS = 10

[DATABASE]
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = cy_arcade
DB_USER = postgres
DB_PASSWORD = votre_mot_de_passe

[LOGGING]
LOG_FILE = server.log
```

**Paramètres serveur :**
- `HOST` : Adresse d'écoute (0.0.0.0 = toutes interfaces, localhost = local uniquement)
- `PORT` : Port d'écoute (1024-65535)
- `TIMEOUT` : Timeout client en secondes
- `MAX_COMMANDS` : Nombre maximum de commandes par connexion

**Paramètres base de données :**
- `DB_HOST` : Adresse du serveur PostgreSQL
- `DB_PORT` : Port PostgreSQL (défaut : 5432)
- `DB_NAME` : Nom de la base de données
- `DB_USER` : Utilisateur PostgreSQL
- `DB_PASSWORD` : Mot de passe

### Client (`client/client.conf`)

```ini
host = localhost
port = 50001
borne_id = 1
```

**Paramètres client :**
- `host` : Adresse du serveur
- `port` : Port du serveur
- `borne_id` : Identifiant de la borne d'arcade

## Installation

### Prérequis

**Serveur (Python) :**
```bash
pip install psycopg2-binary
```

**Client (Java) :**
- JDK 8 ou supérieur

### Lancer le serveur

```bash
python server.py
```

### Lancer le client

```bash
# Compiler
javac ArcadeClient.java SocketConnexion.java

# Exécuter
java ArcadeClient
```

## Protocole de communication

### Commandes disponibles

Une fois le client lancé :
```
> help                          # Afficher l'aide
> PSEUDO 123456                 # Authentification
> BALANCE 123456                # Consulter le solde
> START_GAME 123456 1 2         # Lancer une partie
> END_GAME 123456 1 2 3500      # Terminer avec score
> REWARD 123456                 # Récupérer récompense
> RANKING 2                     # Voir le classement
> RECHARGE 123456 50 CB         # Recharger 50 jetons
> disconnect                    # Se déconnecter
> quit                          # Quitter
```

## Tests

### Test avec netcat (serveur)

```bash
# Lancer le serveur
python server.py

# Lancer le client netcat
ncat localhost 50001
```

### Test avec netcat (client)

```bash
# Lancer un serveur netcat
ncat -l 50001

# Lancer le client Java
java ArcadeClient
```

## Sécurité

- Timeout client : 30 secondes par défaut
- Limite de commandes : 5 par connexion
- Validation des entrées côté serveur
- Gestion des erreurs de connexion
- Logs détaillés des actions

## Logs

Les logs sont automatiquement générés dans :
- **Serveur** : `server/server.log`
- **Client** : `client/client.log`

## Équipe

- **Mathéo COSTA** : matheo.costa4@etu.cyu.fr
- **Tenzin ZURKHANG** : tenzin-rigsang.zurkhang@etu.cyu.fr
- **YANG Kaiwei** : --

## Documentation

- **Rapport complet** : `doc/rapport.pdf`

## Licence

Projet académique - CY Cergy Paris Université © 2025-2026
