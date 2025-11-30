<?php session_start(); ?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion</title>
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
        </ul>
    </nav>
</header>

<main>
	<section>
		<h2>Connexion</h2>

		<?php if (isset($_GET['error'])): ?>
			<p style="color:red;font-weight:bold;">Identifiants incorrects</p>
		<?php endif; ?>

		<form action="verif.php" method="POST">
			<label>Identifiant :</label>
			<input type="text" name="username" required>

			<label>Mot de passe :</label>
			<input type="password" name="password" required>

			<button type="submit">Se connecter</button>
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