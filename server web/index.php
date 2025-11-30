<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Cy_Arcade - Accueil</title>
    <link rel="stylesheet" href="styles.css"/>
</head>
<body>

<header>
    <nav class="navbar">
		<div class="logo">
			<a href="index.php">
				<img src="./images/logo.png" alt="Logo Cy_Arcade">
			</a>
		</div>
        <ul class="nav-links">
            <li><a href="index.php">Accueil</a></li>
            <li><a href="connexion.php">Connexion</a></li>
        </ul>
    </nav>
</header>

<main>

    <!-- Section intro -->
    <section>
        <h1>Cy_Arcade</h1>
        <p><strong>Système de gestion de bornes d'arcade connecté</strong></p>
        <p>Projet de programmation réseau – L3 Informatique – CY Cergy Paris Université (2025-2026)</p>
    </section>

    <!-- Description du projet -->
    <section>
        <h2>Présentation du projet</h2>
        <p>
            Cy_Arcade est un système client-serveur TCP permettant de gérer des bornes d’arcade connectées à une base de données PostgreSQL.
            Le protocole de communication utilise des messages textuels délimités par <code>\n</code>.
        </p>
        <ul>
            <li>Authentification des joueurs via leur carte</li>
            <li>Gestion du solde de jetons</li>
            <li>Lancement et fin de parties</li>
            <li>Calcul des récompenses</li>
            <li>Affichage des classements</li>
            <li>Rechargement du compte</li>
        </ul>
    </section>

    <!-- Architecture -->
    <section>
        <h2>Architecture</h2>
        <pre style="white-space: pre-wrap; font-size: 14px; background:#fafafa; padding:10px; border-radius:8px;">
┌─────────────┐         TCP          ┌─────────────┐         SQL          ┌─────────────┐
│   Client    │ ◄──────────────────► │   Serveur   │ ◄──────────────────► │ PostgreSQL  │
│   (Java)    │   Protocole custom   │   (Python)  │                      │             │
└─────────────┘                      └─────────────┘                      └─────────────┘
        </pre>
    </section>

    <!-- Technologies utilisées -->
    <section>
        <h2>Technologies utilisées</h2>
        <ul>
            <li><strong>Client :</strong> Java (JDK 8+)</li>
            <li><strong>Serveur :</strong> Python 3.7+</li>
            <li><strong>Base de données :</strong> PostgreSQL</li>
            <li><strong>Communication :</strong> TCP</li>
        </ul>
    </section>

    <!-- Structure du projet -->
    <section>
        <h2>Structure du projet</h2>
        <pre style="white-space: pre-wrap; font-size: 14px; background:#fafafa; padding:10px; border-radius:8px;">
Cy_Arcade/
├── server/
│   ├── server.conf
│   ├── server.py
│   └── server.log
├── client/
│   ├── ArcadeClient.java
│   └── SocketConnexion.java
└── doc/
    └── rapport.pdf
        </pre>
    </section>

</main>

<footer>
    <ul>
        <li>©GROUP D4 — CY Cergy Paris Université</li>
    </ul>
</footer>

</body>
</html>
