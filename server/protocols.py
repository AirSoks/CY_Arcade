"""
protocols.py – Gestion des protocoles
"""

import logging
import sys
from utils import (
    send_response, 
    validate_id, 
    validate_positive_int, 
    parse_command, 
    expect_command, 
    verify_card_id
)
from queries import (
    query_pseudo, 
    query_balance,
    query_start_game,
    query_end_game,
    query_reward,
    query_ranking,
    query_recharge,
    query_start_borne
)

MIN_MONTANT = 1
MAX_MONTANT = 500
MIN_SCORE = 0
MAX_SCORE = sys.maxsize
MODES_PAIEMENT = ['CB', 'espece']


def protocol_start(client_socket, db_conn, first_command):
    """Protocole START : PSEUDO → BALANCE → START_GAME"""
    logging.info("Début du protocole START")
    
    try:
        # Étape 1 : PSEUDO
        parts = parse_command(first_command, "PSEUDO", 2)
        id_carte = parts[1]
        id_carte_int = validate_id(id_carte, "CARD_ID")
        
        pseudo = query_pseudo(db_conn, id_carte)
        send_response(client_socket, f"OK {pseudo}")

        # Étape 2 : BALANCE
        parts = expect_command(client_socket, "BALANCE", 2)
        verify_card_id(parts, id_carte)
        
        balance = query_balance(db_conn, id_carte)
        send_response(client_socket, f"OK {balance}")

        # Étape 3 : START_GAME
        parts = expect_command(client_socket, "START_GAME", 4)
        verify_card_id(parts, id_carte)
        
        id_borne = parts[2]
        id_jeux = parts[3]
        
        id_borne_int = validate_id(id_borne, "BORNE_ID")
        id_jeux_int = validate_id(id_jeux, "GAME_ID")
        
        query_start_game(db_conn, id_carte, id_borne, id_jeux)
        send_response(client_socket, "OK")

        logging.info("Protocole START terminé avec succès")
        return "SUCCESS"
        
    except ValueError as e:
        return str(e)
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        return "ERROR DATABASE_ERROR"


def protocol_end(client_socket, db_conn, first_command):
    """Protocole END : END_GAME → REWARD"""
    logging.info("Début du protocole END")
    
    try:
        # Étape 1 : END_GAME
        parts = parse_command(first_command, "END_GAME", 5)
        
        id_carte = parts[1]
        id_borne = parts[2]
        id_jeux = parts[3]
        score = parts[4]
        
        id_carte_int = validate_id(id_carte, "CARD_ID")
        id_borne_int = validate_id(id_borne, "BORNE_ID")
        id_jeux_int = validate_id(id_jeux, "GAME_ID")
        score_int = validate_positive_int(score, MIN_SCORE, MAX_SCORE, "ERROR INVALID_SCORE")
        
        query_end_game(db_conn, id_carte, id_borne, id_jeux, score_int)
        send_response(client_socket, "OK")

        # Étape 2 : REWARD
        parts = expect_command(client_socket, "REWARD", 2)
        verify_card_id(parts, id_carte)
        
        points_gagnes, nouveau_solde = query_reward(db_conn, id_carte)
        send_response(client_socket, f"OK {points_gagnes} {nouveau_solde}")

        logging.info("Protocole END terminé avec succès")
        return "SUCCESS"
        
    except ValueError as e:
        return str(e)
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        return "ERROR DATABASE_ERROR"


def protocol_ranking(client_socket, db_conn, first_command):
    """Protocole RANKING : Récupère le classement"""
    logging.info("Début du protocole RANKING")

    try:
        parts = parse_command(first_command, "RANKING", 2)
        id_jeux = parts[1]
        id_jeux_int = validate_id(id_jeux, "GAME_ID")
        
        ranking_data = query_ranking(db_conn, id_jeux)
        send_response(client_socket, f"OK {ranking_data}")
        
        logging.info("Protocole RANKING terminé avec succès")
        return "SUCCESS"
        
    except ValueError as e:
        return str(e)
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        return "ERROR DATABASE_ERROR"


def protocol_recharge(client_socket, db_conn, first_command):
    """Protocole RECHARGE : Recharge le compte"""
    logging.info("Début du protocole RECHARGE")

    try:
        parts = parse_command(first_command, "RECHARGE", 4)
        
        id_carte = parts[1]
        montant = parts[2]
        mode = parts[3]
        
        id_carte_int = validate_id(id_carte, "CARD_ID")
        montant_int = validate_positive_int(montant, MIN_MONTANT, MAX_MONTANT, "ERROR INVALID_AMOUNT")
        
        if mode not in MODES_PAIEMENT:
            raise ValueError("ERROR INVALID_PAYMENT_MODE")
        
        nouveau_solde = query_recharge(db_conn, id_carte, montant_int, mode)
        send_response(client_socket, f"OK {nouveau_solde}")

        logging.info("Protocole RECHARGE terminé avec succès")
        return "SUCCESS"
        
    except ValueError as e:
        return str(e)
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        return "ERROR DATABASE_ERROR"


def protocol_start_borne(client_socket, db_conn, first_command):
    """Protocole START_BORNE : Initialise une borne"""
    logging.info("Début du protocole START_BORNE")

    try:
        parts = parse_command(first_command, "START_BORNE", 2)
        id_borne = parts[1]
        id_borne_int = validate_id(id_borne, "BORNE_ID")
        
        jeux_data = query_start_borne(db_conn, id_borne)
        send_response(client_socket, f"OK {jeux_data}")

        logging.info("Protocole START_BORNE terminé avec succès")
        return "SUCCESS"
        
    except ValueError as e:
        return str(e)
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        return "ERROR DATABASE_ERROR"