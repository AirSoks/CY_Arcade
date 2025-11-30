"""
server.py — Serveur principal Cy_Arcade
"""

import socket
import logging

from utils import (
    load_config, 
    setup_logging, 
    get_db_connection, 
    send_response, 
    receive_command
)
from protocols import (
    protocol_start,
    protocol_end,
    protocol_ranking,
    protocol_recharge,
    protocol_start_borne
)


config = load_config()
setup_logging(config['LOG_FILE'])

# ============================================================
# CONSTANTES
# ============================================================

SERVER_IP = config['SERVER_IP']
SERVER_PORT = config['SERVER_PORT']
CLIENT_TIMEOUT = config['CLIENT_TIMEOUT']


# ============================================================
# GESTION DES PROTOCOLES
# ============================================================

def handle_protocol(client_socket, db_conn):
    """Dispatcher des protocoles selon la commande reçue"""
    command = receive_command(client_socket)
    if not command:
        return False

    cmd = command.split()[0].upper()
    logging.info(f"Commande reçue : {cmd}")

    if cmd == "PSEUDO":
        result = protocol_start(client_socket, db_conn, command)
    elif cmd == "END_GAME":
        result = protocol_end(client_socket, db_conn, command)
    elif cmd == "RANKING":
        result = protocol_ranking(client_socket, db_conn, command)
    elif cmd == "RECHARGE":
        result = protocol_recharge(client_socket, db_conn, command)
    elif cmd == "START_BORNE":
        result = protocol_start_borne(client_socket, db_conn, command)
    else:
        logging.warning(f"Protocole inconnu : {cmd}")
        send_response(client_socket, "ERROR UNKNOWN_PROTOCOL")
        return False

    # Vérifier si le protocole a renvoyé une erreur
    if isinstance(result, str) and result.startswith("ERROR"):
        logging.warning(f"Protocole échoué : {result}")
        send_response(client_socket, result)
        return False

    return True


# ============================================================
# GESTION DU CLIENT
# ============================================================

def handle_client(client_socket, client_address, db_conn):
    """Gère un client - UN SEUL protocole puis déconnexion"""
    logging.info(f"=== Nouvelle connexion depuis {client_address} ===")

    client_socket.settimeout(CLIENT_TIMEOUT)

    try:
        success = handle_protocol(client_socket, db_conn)
        
        if not success:
            logging.warning(f"Session échouée pour {client_address}")
        else:
            logging.info(f"Session réussie pour {client_address}")

    except Exception as e:
        logging.error(f"Erreur durant la session : {e}")

    finally:
        client_socket.close()
        logging.info(f"=== Connexion fermée : {client_address} ===\n")


# ============================================================
# SERVEUR PRINCIPAL
# ============================================================

def run_server():
    """Lance le serveur principal"""
    logging.info("=" * 50)
    logging.info("Démarrage du serveur Cy_Arcade")
    logging.info("=" * 50)

    # Connexion à la BD
    db_conn = get_db_connection(config)
    if db_conn is None:
        logging.critical("Impossible de démarrer sans connexion BD")
        return

    # Création du socket serveur
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((SERVER_IP, SERVER_PORT))
    except OSError as e:
        logging.critical(f"Port {SERVER_PORT} déjà utilisé : {e}")
        return

    server.listen(0)

    logging.info(f"Serveur en écoute sur {SERVER_IP}:{SERVER_PORT}")
    logging.info("En attente de connexions...\n")

    try:
        while True:
            # Accepter une nouvelle connexion
            client_socket, client_address = server.accept()
            handle_client(client_socket, client_address, db_conn)

    except Exception as e:
        logging.critical(f"Erreur fatale : {e}")
    finally:
        db_conn.close()
        server.close()
        logging.info("Serveur arrêté")


if __name__ == "__main__":
    run_server()
