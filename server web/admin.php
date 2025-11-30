<?php
require_once __DIR__ . '/config/config.php';

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'admin') {
    header("Location: index.php");
    exit();
}

//Statistiques
$s1 = pg_fetch_assoc(pg_query($db, "SELECT COUNT(*) AS total FROM Client"));
$s2 = pg_fetch_assoc(pg_query($db, "SELECT COUNT(*) AS total FROM Borne"));
$s3 = pg_fetch_assoc(pg_query($db, "SELECT COUNT(*) AS total FROM Partie"));
$s4 = pg_fetch_assoc(pg_query($db, "SELECT COUNT(*) AS total FROM Carte"));
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Admin</title>
<link rel="stylesheet" href="styles.css">
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
            <li><a href="logout.php">Déconnexion</a></li>
        </ul>
    </nav>
</header>

<main>
	<section>
		<h2>Interface Administrateur</h2>

		<p>Clients inscrits : <?= $s1['total'] ?></p>
		<p>Bornes installées : <?= $s2['total'] ?></p>
		<p>Parties jouées : <?= $s3['total'] ?></p>
		<p>Cartes émises : <?= $s4['total'] ?></p>

		<a href="gestion_systeme.php">Gestion Bornes & Jeux</a>
	</section>
</main>

<footer>
    <ul>
        <li>©GROUP D4 — CY Cergy Paris Université</li>
    </ul>
</footer>

</body>
</html>
