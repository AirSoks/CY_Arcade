<?php
require_once __DIR__ . '/config/config.php';

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'admin') {
    header("Location: index.php");
    exit();
}

$message = "";

// Update borne
if (isset($_POST['update_borne'])) {
    $id_borne = $_POST['id_borne'];
    $etat = $_POST['etat_borne'];

    $q = "UPDATE Borne SET etat_borne = $1 WHERE id_borne = $2";
    if (pg_query_params($db, $q, array($etat, $id_borne))) {
        $message = "<p style='color:green;font-weight:bold;'> État de la borne mis à jour</p>";
    } else {
        $message = "<p style='color:red;'> Erreur lors de la mise à jour</p>";
    }
}

// Update jeu
if (isset($_POST['update_jeu'])) {
    $id_jeu = $_POST['id_jeu'];
    $etat = $_POST['etat_jeu'];

    $q = "UPDATE Jeux SET etat_jeu = $1 WHERE id_jeux = $2";
    if (pg_query_params($db, $q, array($etat, $id_jeu))) {
        $message = "<p style='color:green;font-weight:bold;'> État du jeu mis à jour</p>";
    } else {
        $message = "<p style='color:red;'> Erreur lors de la mise à jour</p>";
    }
}

$bornes = pg_query($db, "SELECT id_borne, etat_borne FROM Borne ORDER BY id_borne ASC");
$jeux = pg_query($db, "SELECT id_jeux, nom, etat_jeu FROM Jeux ORDER BY id_jeux ASC");
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Gestion Bornes & Jeux</title>
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
            <li><a href="admin.php">Retour Admin</a></li>
            <li><a href="logout.php">Déconnexion</a></li>
        </ul>
    </nav>
</header>

<main>
	<section>
		<h2>Gestion de la Salle d'Arcade</h2>
		<?php echo $message; ?>
		
		<hr><br>
		<h3>Modifier l’état d’une borne</h3>

		<form method="POST">
			<select name="id_borne" required>
			<?php while ($b = pg_fetch_assoc($bornes)): ?>
				<option value="<?= $b['id_borne'] ?>">Borne #<?= $b['id_borne'] ?> (<?= $b['etat_borne'] ?>)</option>
			<?php endwhile; ?>
			</select>

			<select name="etat_borne" required>
				<option value="Disponible">Disponible</option>
				<option value="En Maintenance">En Maintenance</option>
				<option value="HS">HS</option>
			</select>

			<button type="submit" name="update_borne">Mettre à jour</button>
		</form>

		<hr><br>
		<h3>Modifier l’état d’un jeu</h3>

		<form method="POST">
			<select name="id_jeu" required>
			<?php while ($j = pg_fetch_assoc($jeux)): ?>
				<option value="<?= $j['id_jeux'] ?>"><?= $j['nom'] ?> (<?= $j['etat_jeu'] ?>)</option>
			<?php endwhile; ?>
			</select>

			<select name="etat_jeu" required>
				<option value="Disponible">Disponible</option>
				<option value="En Maintenance">En Maintenance</option>
				<option value="HS">HS</option>
			</select>

			<button type="submit" name="update_jeu">Mettre à jour</button>
		</form>

	</section>
</main>

<footer>
	<ul><li>©GROUP D4 — CY Cergy Paris Université</li></ul>
</footer>

</body>
</html>