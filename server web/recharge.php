<?php
require_once __DIR__ . '/config/config.php';

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'client') {
    header("Location: index.php");
    exit();
}

$id_client = $_SESSION['id_client'];

$montant = intval($_POST['montant_jetons']);

// Récupération de la carte actuelle
$q_carte = "
    SELECT id_carte FROM Carte 
    WHERE id_client = $1 
    ORDER BY date_carte DESC LIMIT 1";
$r_carte = pg_fetch_assoc(pg_query_params($db, $q_carte, array($id_client)));

$id_carte = $r_carte['id_carte'] ?? null;
if (!$id_carte) {
    header("Location: profile.php?msg=nocarte");
    exit();
}

// Mise à jour solde client
$q_update = "UPDATE Client SET solde_jetons = solde_jetons + $1 WHERE id_client = $2";
pg_query_params($db, $q_update, array($montant, $id_client));

// Ajout ligne dans Recharge
$q_insert = "INSERT INTO Recharge (montant_jeton, mode_paiement, date_recharge, id_carte)
             VALUES ($1, 'CB', CURRENT_DATE, $2)";
pg_query_params($db, $q_insert, array($montant, $id_carte));

header("Location: profile.php?success=1");
exit();
