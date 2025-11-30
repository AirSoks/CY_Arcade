# Cy_Arcade - Système de Gestion de Bornes d'Arcade

> Projet de programmation réseau - L3 Informatique  
> CY Cergy Paris Université | 2025-2026

## À propos

Cy_Arcade est un système client-serveur TCP permettant de gérer des bornes d'arcade connectées à une base de données PostgreSQL. Le projet implémente un protocole de communication personnalisé pour gérer l'authentification, les parties, les récompenses et les classements.

## Architecture

```
┌─────────────┐         TCP          ┌─────────────┐         SQL          ┌─────────────┐
│   Client    │ ◄──────────────────► │   Serveur   │ ◄──────────────────► │  PostgreSQL │
│   (Java)    │   Protocole custom   │   (Python)  │                      │             │
└─────────────┘                      └─────────────┘                      └─────────────┘
															                     ▲ 
														                         │
								  ┌────────────────┐                             │
								  │  Interface Web │ ◄───────────────────────────┘
							      │     (PHP)      │ 
							      └────────────────┘
```

Le système repose sur une architecture comme ceci :
- Le **client Java** gère l'interface utilisateur et les interactions avec les bornes d'arcade
- Le **serveur Python** orchestre la logique métier et valide les protocoles de communication
- L'**interface web PHP** permet la gestion administrative et la consultation des profils utilisateurs
- La **base PostgreSQL** centralise toutes les données (joueurs, parties, scores, transactions)

## Fonctionnalités

### Système de bornes (Client Java + Serveur Python)

**START** - Démarrage de partie
- Authentification du joueur via carte
- Vérification du solde
- Débit des jetons et lancement de la partie

**END** - Fin de partie et récompenses
- Enregistrement du score
- Calcul automatique des récompenses selon le score
- Mise à jour du solde

**RANKING** - Classements
- Top 3 des meilleurs scores par jeu

**RECHARGE** - Gestion du compte
- Recharge de jetons (CB ou espèces)

**START_BORNE** - Initialisation
- Récupération des jeux disponibles

### Interface web (PHP)

**Espace Client**
- Consultation du profil (pseudo, solde, statistiques)
- Historique des parties jouées
- Recharge de jetons en ligne

**Espace Administrateur**
- Dashboard avec statistiques globales (clients, bornes, parties)
- Gestion de l'état des bornes (Disponible, En Maintenance, HS)
- Gestion de l'état des jeux

### Technologies

- **Client bornes** : Java 8+
- **Serveur métier** : Python 3.7+ avec psycopg2
- **Interface web** : PHP 7+
- **Base de données** : PostgreSQL
- **Communication** : Protocole custom sur TCP

## Structure du projet

```
Cy_Arcade/
├── server/
│   ├── server.py          # Serveur TCP principal
│   ├── protocols.py       # Gestion des 5 protocoles
│   ├── queries.py         # Requêtes SQL et logique métier
│   ├── utils.py           # Validation, configuration, logging
│   └── server.conf        # Configuration (serveur + BD)
├── client/
│   ├── ArcadeClient.java      # Interface utilisateur
│   ├── SocketConnexion.java   # Abstraction socket + logs
│   ├── ClientConfig.java      # Gestion configuration
│   └── client.conf            # Paramètres (host, port, borne_id)
├── web/
│   ├── index.php              # Page d'accueil
│   ├── connexion.php          # Authentification
│   ├── profile.php            # Profil client
│   ├── admin.php              # Dashboard admin
│   ├── gestion_systeme.php    # Gestion bornes/jeux
│   ├── recharge.php           # Recharge de jetons
│   ├── verif.php              # Vérification credentials
│   ├── logout.php             # Déconnexion
│   ├── styles.css             # Styles
│   └── config/
│       └── config.php         # Configuration BD
├── SQL/
│   ├── DDL.sql            # Schéma de la base
│   └── DML.sql            # Données de test
└── doc/
    └── rapport.pdf        # Documentation complète
```

## Configuration

### Serveur (`server/server.conf`)

```ini
[SERVER]
HOST = 0.0.0.0
PORT = 50001
TIMEOUT = 30
MAX_COMMANDS = 5

[DATABASE]
DB_HOST = ******
DB_PORT = 5432
DB_NAME = ******
DB_USER = ******
DB_PASSWORD = ******

[LOGGING]
LOG_FILE = server/server.log
```

### Client (`client/client.conf`)

```ini
host = localhost
port = 50001
borne_id = 1
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

## Sécurité et robustesse

**Système de bornes (Java/Python)**
- Timeout client : 30 secondes par défaut
- Limite de commandes : 5 par connexion
- Validation des entrées côté serveur
- Gestion des erreurs de connexion
- Logs détaillés des actions

**Interface web (PHP)**
- Authentification avec mots de passe hashés (`password_hash()` / `password_verify()`)
- Contrôle d'accès basé sur les rôles (Client / Admin)

## Logs

Les logs sont automatiquement générés dans :
- **Serveur** : `server/server.log`
- **Client** : `client/client.log`

## Contributeurs

- **Mathéo COSTA** - matheo.costa4@etu.cyu.fr
- **Tenzin ZURKHANG** - tenzin-rigsang.zurkhang@etu.cyu.fr
- **YANG Kaiwei**

## Documentation

Rapport complet disponible dans [`docs/rapport.pdf`]

## Attentes

Les attendus auto-notés sont disponibles dans [`docs/Grille de notation de projet.pdf`]

---

**Projet académique - CY Cergy Paris Université © 2025-2026**