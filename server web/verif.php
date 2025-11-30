<?php
require_once __DIR__ . '/config/config.php';

$login = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

// Récupérer la personne par login
$q = "SELECT * FROM Personne WHERE login = $1";
$user = pg_fetch_assoc(pg_query_params($db, $q, array($login)));

// Vérifier login + mot de passe hashé
if ($user && password_verify($password, $user['mot_de_passe'])) {

    $_SESSION['id_perso'] = $user['id_perso'];
    $_SESSION['nom'] = $user['nom'];

    $id = $user['id_perso'];

    // Client
    $qc = "SELECT id_client FROM Client WHERE id_client = $1";
    $rc = pg_query_params($db, $qc, array($id));

    if (pg_num_rows($rc) > 0) {
        $_SESSION['role'] = "client";
        $_SESSION['id_client'] = $id;
        header("Location: profile.php");
        exit();
    }

    // Admin
    $qa = "SELECT id_admin FROM Admin WHERE id_admin = $1";
    $ra = pg_query_params($db, $qa, array($id));

    if (pg_num_rows($ra) > 0) {
        $_SESSION['role'] = "admin";
        header("Location: admin.php");
        exit();
    }
}

// Si on arrive ici → erreur
header("Location: connexion.php?error=1");
exit();
