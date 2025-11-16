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
│   ├── server.conf              # Configuration du serveur
│   ├── server.py                # Serveur TCP Python
│   └── server.log               # Logs du serveur (généré automatiquement)
├── client/
│   ├── ArcadeClient.java        # Client Java
│   └── SocketConnexion.java     # Gestion de la connexion TCP
└── doc/
    └── rapport.pdf              # Rapport de projet
```

## Configuration

### Fichier `server.conf`

**Paramètres modifiables :**
- `HOST` : Adresse IP du serveur (0.0.0.0 - localhost pour toutes les interfaces)
- `PORT` : Port d'écoute (1024-65535)
- `TIMEOUT` : Timeout client en secondes
- `MAX_COMMANDS` : Nombre maximum de commandes par connexion

## Lancement

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

### Format des messages

Tous les messages sont terminés par `\n`.

### Codes d'erreur

- `ERROR UNKNOWN_COMMAND` : Commande non reconnue
- `ERROR INVALID_SYNTAX` : Syntaxe incorrecte
- `ERROR TIMEOUT` : Timeout du client
- `ERROR MAX_COMMANDS_REACHED` : Limite de commandes atteinte

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

- Timeout client : 10 secondes par défaut
- Limite de commandes : 5 par connexion
- Validation des entrées côté serveur
- Gestion des erreurs de connexion
- Logs détaillés des actions

## Logs

Les logs sont enregistrés dans `server/server.log` et affichés dans la console.

## Équipe

- **Mathéo COSTA** : matheo.costa4@etu.cyu.fr
- **Tenzin ZURKHANG** : tenzin-rigsang.zurkhang@etu.cyu.fr
- **YANG Kaiwei** : --

## Documentation

- **Rapport complet** : `doc/rapport.pdf`

## Licence

Projet académique - CY Cergy Paris Université © 2025-2026
