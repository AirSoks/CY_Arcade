"""
queries.py – Requêtes de base de données
"""

import logging


def query_pseudo(db_conn, id_carte):
    """Récupère le pseudo associé à la carte"""
    logging.info(f"Récupération du pseudo pour carte {id_carte}")
    
    cursor = db_conn.cursor()
    query = """
    SELECT Client.pseudo
    FROM Carte
    JOIN Client ON Carte.id_client = Client.id_client
    WHERE Carte.id_carte = %s AND Carte.status_carte = 'Liee'
    """
    cursor.execute(query, (id_carte,))
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        logging.warning(f"Carte {id_carte} introuvable")
        raise ValueError("ERROR CARD_NOT_FOUND")

    pseudo = result[0]
    logging.info(f"Pseudo trouvé : {pseudo}")
    return pseudo


def query_balance(db_conn, id_carte):
    """Récupère le solde de la carte"""
    logging.info(f"Consultation du solde pour carte {id_carte}")
    
    cursor = db_conn.cursor()
    query = """
    SELECT Client.solde_jetons
    FROM Carte
    JOIN Client ON Carte.id_client = Client.id_client
    WHERE Carte.id_carte = %s AND Carte.status_carte = 'Liee'
    """
    cursor.execute(query, (id_carte,))
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        logging.warning(f"Carte {id_carte} introuvable")
        raise ValueError("ERROR CARD_NOT_FOUND")

    solde = result[0]
    logging.info(f"Solde actuel : {solde} jetons")
    return solde


def query_start_game(db_conn, id_carte, id_borne, id_jeux):
    """Lance une partie"""
    logging.info(f"Démarrage partie : carte={id_carte}, borne={id_borne}, jeu={id_jeux}")
    
    cursor = db_conn.cursor()

    # Récupérer id_client et solde
    query = """
    SELECT Client.id_client, Client.solde_jetons
    FROM Carte
    JOIN Client ON Carte.id_client = Client.id_client
    WHERE Carte.id_carte = %s AND Carte.status_carte = 'Liee'
    """
    cursor.execute(query, (id_carte,))
    client_result = cursor.fetchone()
    if client_result is None:
        cursor.close()
        logging.warning(f"Carte {id_carte} introuvable")
        raise ValueError("ERROR CARD_NOT_FOUND")

    id_client, solde_jetons = client_result

    # Vérifier que le jeu existe et est disponible
    query = "SELECT Jeux.etat_jeu FROM Jeux WHERE Jeux.id_jeux = %s"
    cursor.execute(query, (id_jeux,))
    jeu_result = cursor.fetchone()
    if jeu_result is None:
        cursor.close()
        logging.warning(f"Jeu {id_jeux} introuvable")
        raise ValueError("ERROR GAME_NOT_FOUND")

    if jeu_result[0] != 'Disponible':
        cursor.close()
        logging.warning(f"Jeu {id_jeux} indisponible")
        raise ValueError("ERROR GAME_UNAVAILABLE")

    # Vérifier la borne
    query = "SELECT Borne.etat_borne, Borne.prix_jeton FROM Borne WHERE Borne.id_borne = %s"
    cursor.execute(query, (id_borne,))
    borne_result = cursor.fetchone()
    if borne_result is None:
        cursor.close()
        logging.warning(f"Borne {id_borne} introuvable")
        raise ValueError("ERROR ARCADE_NOT_FOUND")

    if borne_result[0] != 'Disponible':
        cursor.close()
        logging.warning(f"Borne {id_borne} indisponible")
        raise ValueError("ERROR ARCADE_UNAVAILABLE")

    prix_jeton = borne_result[1]

    # Vérifier le solde
    if solde_jetons < prix_jeton:
        cursor.close()
        logging.warning(f"Solde insuffisant : {solde_jetons} < {prix_jeton}")
        raise ValueError("ERROR INSUFFICIENT_BALANCE")

    # Débiter le compte
    query = "UPDATE Client SET solde_jetons = solde_jetons - %s WHERE id_client = %s"
    cursor.execute(query, (prix_jeton, id_client))

    # Créer l'entrée de partie
    query = """
    INSERT INTO Partie (id_client, id_jeux, id_borne, status_partie, date_partie)
    VALUES (%s, %s, %s, 'En cours', CURRENT_DATE)
    """
    cursor.execute(query, (id_client, id_jeux, id_borne))

    db_conn.commit()
    cursor.close()
    logging.info(f"Partie démarrée avec succès ({prix_jeton} jetons débités)")


def query_end_game(db_conn, id_carte, id_borne, id_jeux, score):
    """Termine une partie"""
    logging.info(f"Fin de partie : carte={id_carte}, score={score}")
    
    cursor = db_conn.cursor()

    # Récupérer id_client
    query = """
    SELECT Client.id_client
    FROM Carte
    JOIN Client ON Carte.id_client = Client.id_client
    WHERE Carte.id_carte = %s
    """
    cursor.execute(query, (id_carte,))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        logging.warning(f"Carte {id_carte} introuvable")
        raise ValueError("ERROR CARD_NOT_FOUND")

    id_client = result[0]

    # Mettre à jour la partie en cours
    query = """
    UPDATE Partie
    SET score = %s, date_partie = CURRENT_DATE, status_partie = 'Termine'
    WHERE id_client = %s AND id_borne = %s AND id_jeux = %s AND status_partie = 'En cours'
    """
    cursor.execute(query, (score, id_client, id_borne, id_jeux))

    if cursor.rowcount == 0:
        cursor.close()
        logging.warning("Aucune partie active trouvée")
        raise ValueError("ERROR NO_ACTIVE_GAME")

    db_conn.commit()
    cursor.close()
    logging.info(f"Partie terminée avec succès")


def query_reward(db_conn, id_carte):
    """Calcule et renvoie la récompense"""
    logging.info(f"Calcul de la récompense pour carte {id_carte}")
    
    cursor = db_conn.cursor()

    # Récupérer id_client
    query = """
    SELECT Client.id_client
    FROM Carte
    JOIN Client ON Carte.id_client = Client.id_client
    WHERE Carte.id_carte = %s
    """
    cursor.execute(query, (id_carte,))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        logging.warning(f"Carte {id_carte} introuvable")
        raise ValueError("ERROR CARD_NOT_FOUND")

    id_client = result[0]

    # Récupérer la dernière partie terminée
    query = """
    SELECT Partie.score, Partie.id_partie
    FROM Partie
    WHERE Partie.id_client = %s AND Partie.status_partie = 'Termine'
    ORDER BY Partie.date_partie DESC, Partie.id_partie DESC
    LIMIT 1
    """
    cursor.execute(query, (id_client,))
    partie_result = cursor.fetchone()
    if partie_result is None:
        cursor.close()
        logging.warning("Aucune partie terminée trouvée")
        raise ValueError("ERROR NO_FINISHED_GAME")

    score, id_partie = partie_result

    # Déterminer la récompense
    recompense = 0
    if score >= 5000:
        recompense = 5
    elif score >= 2000:
        recompense = 2
    elif score >= 1000:
        recompense = 1
    
    if recompense != 0:
        query = """
        UPDATE Client
        SET solde_jetons = solde_jetons + %s
        WHERE id_client = %s
        RETURNING solde_jetons
        """
        cursor.execute(query, (recompense, id_client))
        nouveau_solde = cursor.fetchone()[0]
        logging.info(f"Récompense attribuée : {recompense} jetons (nouveau solde: {nouveau_solde})")
    else:
        query = "SELECT Client.solde_jetons FROM Client WHERE Client.id_client = %s"
        cursor.execute(query, (id_client,))
        nouveau_solde = cursor.fetchone()[0]
        logging.info(f"Aucune récompense")
    
    # Marquer la partie comme récompensée
    query = """
    UPDATE Partie
    SET recompense = %s, status_partie = 'Recompense donnee'
    WHERE id_partie = %s
    """
    cursor.execute(query, (recompense, id_partie))

    db_conn.commit()
    cursor.close()
    return recompense, nouveau_solde


def query_ranking(db_conn, id_jeux):
    """Récupère le top 3 d'un jeu"""
    logging.info(f"Consultation du classement pour jeu {id_jeux}")
    
    cursor = db_conn.cursor()

    # Vérifier que le jeu existe
    query = "SELECT Jeux.id_jeux FROM Jeux WHERE Jeux.id_jeux = %s"
    cursor.execute(query, (id_jeux,))
    if cursor.fetchone() is None:
        cursor.close()
        logging.warning(f"Jeu {id_jeux} introuvable")
        raise ValueError("ERROR GAME_NOT_FOUND")

    # Récupérer le top 3
    query = """
    SELECT Client.pseudo, MAX(Partie.score) AS meilleur_score
    FROM Partie
    JOIN Client ON Partie.id_client = Client.id_client
    WHERE Partie.id_jeux = %s AND Partie.score IS NOT NULL
    GROUP BY Client.pseudo
    ORDER BY meilleur_score DESC
    LIMIT 3
    """
    cursor.execute(query, (id_jeux,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        logging.warning(f"Aucun classement disponible pour jeu {id_jeux}")
        raise ValueError("ERROR NO_RANKING")

    # Format : rank:pseudo:score,rank:pseudo:score,...
    ranking_parts = []
    for i, (pseudo, score) in enumerate(results, 1):
        ranking_parts.append(f"{i} {pseudo} {score}")
    ranking_data = ", ".join(ranking_parts)

    logging.info(f"Classement récupéré : {len(results)} entrée(s)")
    return ranking_data


def query_recharge(db_conn, id_carte, montant, mode_paiement):
    """Recharge les jetons d'un client"""
    logging.info(f"Recharge : carte={id_carte}, montant={montant}, mode={mode_paiement}")
    
    cursor = db_conn.cursor()

    # Récupérer id_client
    query = """
    SELECT Client.id_client
    FROM Carte
    JOIN Client ON Carte.id_client = Client.id_client
    WHERE Carte.id_carte = %s AND Carte.status_carte = 'Liee'
    """
    cursor.execute(query, (id_carte,))
    result = cursor.fetchone()
    if result is None:
        cursor.close()
        logging.warning(f"Carte {id_carte} introuvable")
        raise ValueError("ERROR CARD_NOT_FOUND")

    id_client = result[0]

    # Enregistrer la recharge
    query = """
    INSERT INTO Recharge (id_carte, montant_jeton, mode_paiement, date_recharge)
    VALUES (%s, %s, %s, CURRENT_DATE)
    """
    cursor.execute(query, (id_carte, montant, mode_paiement))

    # Mettre à jour le solde
    query = """
    UPDATE Client
    SET solde_jetons = solde_jetons + %s
    WHERE id_client = %s
    RETURNING solde_jetons
    """
    cursor.execute(query, (montant, id_client))
    nouveau_solde = cursor.fetchone()[0]

    db_conn.commit()
    cursor.close()
    logging.info(f"Recharge effectuée : nouveau solde = {nouveau_solde} jetons")
    return nouveau_solde


def query_start_borne(db_conn, id_borne):
    """Récupère les infos de la borne et les jeux disponibles"""
    logging.info(f"Initialisation de la borne {id_borne}")
    
    cursor = db_conn.cursor()

    # Vérifier que la borne existe
    query = "SELECT Borne.etat_borne FROM Borne WHERE Borne.id_borne = %s"
    cursor.execute(query, (id_borne,))
    borne_result = cursor.fetchone()
    if borne_result is None:
        cursor.close()
        logging.warning(f"Borne {id_borne} introuvable")
        raise ValueError("ERROR ARCADE_NOT_FOUND")

    if borne_result[0] != 'Disponible':
        cursor.close()
        logging.warning(f"Borne {id_borne} indisponible")
        raise ValueError("ERROR ARCADE_UNAVAILABLE")

    # Récupérer les jeux disponibles
    query = "SELECT Jeux.id_jeux, Jeux.nom FROM Jeux WHERE Jeux.etat_jeu = 'Disponible'"
    cursor.execute(query)
    jeux_results = cursor.fetchall()
    cursor.close()

    if not jeux_results:
        logging.warning("Aucun jeu disponible")
        raise ValueError("ERROR NO_GAMES_AVAILABLE")

    # Format : id_jeu:nom_jeu
    jeux_parts = []
    for id_jeu, nom_jeu in jeux_results:
        jeux_parts.append(f"{id_jeu}:{nom_jeu}")
    jeux_data = ",".join(jeux_parts)

    logging.info(f"Borne initialisée : {len(jeux_results)} jeu(x) disponible(s)")
    return jeux_data