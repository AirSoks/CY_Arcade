<?php
require_once __DIR__ . '/config/config.php';

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'client') {
    header("Location: index.php");
    exit();
}

$id = $_SESSION['id_client'];

//Infos client
$user_q = "SELECT pseudo, solde_jetons FROM Client WHERE id_client = $1";
$user = pg_fetch_assoc(pg_query_params($db, $user_q, array($id)));

//Cartes
$cards_q = "SELECT version_carte FROM Carte WHERE id_client = $1";
$cards_res = pg_query_params($db, $cards_q, array($id));
$versions = [];
while ($row = pg_fetch_assoc($cards_res)) {
    $versions[] = $row['version_carte'];
}

//Parties + dernière partie
$games_q = "
    SELECT COUNT(*) AS nb_parties, MAX(date_partie) AS derniere
    FROM Partie WHERE id_client = $1
";
$games = pg_fetch_assoc(pg_query_params($db, $games_q, array($id)));

// Jeu le plus joué
$q_top = "
    SELECT j.nom, COUNT(*) AS nb
    FROM Partie p
    JOIN Jeux j ON p.id_jeux = j.id_jeux
    WHERE p.id_client = $1
    GROUP BY j.nom
    ORDER BY nb DESC
    LIMIT 1
";
$r_top = pg_query_params($db, $q_top, array($id));
$top = pg_fetch_assoc($r_top);

// Meilleur score
$q_best = "SELECT MAX(score) AS best FROM Partie WHERE id_client = $1";
$r_best = pg_query_params($db, $q_best, array($id));
$best = pg_fetch_assoc($r_best);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8"><title>Mon Profil</title>
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
		<?php if (isset($_GET['success'])): ?>
			<p style="color:green;font-weight:bold;">Recharge effectuée</p>
		<?php endif; ?>
		<h1>Mon Profil</h1>

		<p><strong>Pseudo :</strong> <?= $user['pseudo'] ?></p>
		<p><strong>Solde :</strong> <?= $user['solde_jetons'] ?> jetons</p>
		<p><strong>Version carte(s) :</strong> <?php echo implode(", ", $versions); ?></p>
		<p><strong>Parties jouées :</strong> <?= $games['nb_parties'] ?></p>
		<p><strong>Dernière partie :</strong> <?= $games['derniere'] ?? "Jamais" ?></p>
		<p><strong>Meilleur score :</strong> <?= $best['best'] ?? "Aucun" ?></p>
		<p><strong>Jeu le plus joué :</strong> <?= $top['nom'] ?? "Aucun" ?></p>

	</section>
	<section>
		<h3>Recharger mes jetons</h3>
		<form action="recharge.php" method="POST">
			<label>Montant :</label>
			<select name="montant_jetons" required>
				<option value="10">10 jetons</option>
				<option value="20">20 jetons</option>
				<option value="50">50 jetons</option>
				<option value="100">100 jetons</option>
			</select>

			<button type="submit">Recharger</button>
		</form>
	</section>
</main>

<footer>
    <ul>
        <li>©GROUP D4 — CY Cergy Paris Université</li>
    </ul>
</footer>

</body>
</html>