"""
Serveur TCP
"""

import sys
import socket
import logging
import psycopg2
import configparser

# ============================================================
# CONFIGURATION
# ============================================================

def load_config(config_file):
    """Charge la configuration du serveur et de la base de données"""
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    config_values = {
        'SERVER_IP': config.get('SERVER', 'HOST'),
        'SERVER_PORT': config.getint('SERVER', 'PORT'),
        'CLIENT_TIMEOUT': config.getint('SERVER', 'TIMEOUT'),
        'MAX_COMMANDS': config.getint('SERVER', 'MAX_COMMANDS'),

        'DB_HOST': config.get('DATABASE', 'HOST'),
        'DB_PORT': config.getint('DATABASE', 'PORT'),
        'DB_NAME': config.get('DATABASE', 'NAME'),
        'DB_USER': config.get('DATABASE', 'USER'),
        'DB_PASSWORD': config.get('DATABASE', 'PASSWORD'),
        
        'LOG_FILE': config.get('LOGGING', 'LOG_FILE')
    }
    return config_values

def setup_logging(log_file):
    """Configure le logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Handler fichier
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

config = load_config("server.conf")
setup_logging(config['LOG_FILE'])

SERVER_IP = config['SERVER_IP']
SERVER_PORT = config['SERVER_PORT']
CLIENT_TIMEOUT = config['CLIENT_TIMEOUT']
MAX_COMMANDS = config['MAX_COMMANDS']

DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_NAME = config['DB_NAME']
DB_USER = config['DB_USER']
DB_PASSWORD = config['DB_PASSWORD']

logging.info("Configuration chargée depuis")

# ============================================================
# GESTION DES COMMANDES
# ============================================================

def handle_pseudo(id_carte):
    """Récupère le pseudo associé à la carte"""
    logging.debug(f"Handler PSEUDO pour carte {id_carte}")
    # TODO : requête SQL
    return "OK Reponse de la requete PSEUDO ici"


def handle_balance(id_carte):
    """Récupère le solde de la carte"""
    logging.debug(f"Handler BALANCE pour carte {id_carte}")
    # TODO : requête SQL
    return "OK Reponse de la requete BALANCE ici"


def handle_start_game(id_carte, id_borne, id_jeux):
    """Lance une partie"""
    logging.debug(f"Handler START_GAME : carte={id_carte}, borne={id_borne}, jeu={id_jeux}")
    # TODO : requête SQL
    return "OK Reponse de la requete START_GAME ici"


def handle_end_game(id_carte, id_borne, id_jeux, score):
    """Termine une partie"""
    logging.debug(f"Handler END_GAME : carte={id_carte}, score={score}")
    # TODO : requête SQL
    return "OK Reponse de la requete END_GAME ici"


def handle_reward(id_carte):
    """Calcule et renvoie la récompense"""
    logging.debug(f"Handler REWARD pour carte {id_carte}")
    # TODO : requête SQL
    return "OK Reponse de la requete REWARD ici"


def handle_ranking(id_jeux):
    """Récupère le top 3 d'un jeu"""
    logging.debug(f"Handler RANKING pour jeu {id_jeux}")
    # TODO : requête SQL
    return "OK reponse de la requete RANKING ici"


def handle_recharge(id_carte, montant_jeton, mode_paiement):
    """Recharge les jetons d'un client"""
    logging.debug(f"Handler RECHARGE : carte={id_carte}, montant={montant_jeton}, mode={mode_paiement}")
    # TODO : requête SQL
    return "OK reponse de la requete RECHARGE ici"


def handle_start_borne(id_borne):
    """Initialise une borne et renvoie ses infos + la liste des jeux"""
    logging.debug(f"Handler START_BORNE pour borne {id_borne}")
    # TODO : requête SQL
    return "OK reponse de la requete START_BORNE ici"


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def get_db_connection():
    """Connexion à la base de données"""
    try:
        db_connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logging.info("Connexion à la BD réussie")
        return db_connection
    except Exception as e:
        logging.critical(f"Erreur de connexion à la BD : {e}")
        return None


def receive_command(client_socket):
    """Reçoit une commande du client"""
    try:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            return None
        command = data.split('\n')[0].strip()
        return command
    except socket.timeout:
        logging.warning("Timeout : le client n'a pas répondu")
        return None
    except Exception as e:
        logging.error(f"Erreur de réception : {e}")
        return None


def send_response(client_socket, response):
    """Envoie une réponse au client"""
    try:
        client_socket.send((response + "\n").encode("utf-8"))
        logging.debug(f"Réponse envoyée : {response}")
    except Exception as e:
        logging.error(f"Erreur d'envoi : {e}")


# ============================================================
# TRAITEMENT DES COMMANDES
# ============================================================

def process_command(command):
    """Parse et traite une commande"""
    parts = command.split()
    
    if not parts:
        return "ERROR EMPTY_COMMAND"
    
    command_name = parts[0].upper()
    
    commands = {
        "PSEUDO": (2, handle_pseudo),
        "BALANCE": (2, handle_balance),
        "START_GAME": (4, handle_start_game),
        "END_GAME": (5, handle_end_game),
        "REWARD": (2, handle_reward),
        "RANKING": (2, handle_ranking),
        "RECHARGE": (4, handle_recharge),
        "START_BORNE": (2, handle_start_borne),
    }
    
    if command_name not in commands:
        logging.warning(f"Commande inconnue : {command_name}")
        return "ERROR UNKNOWN_COMMAND"
    
    expected_args, handler = commands[command_name]
    
    if len(parts) != expected_args:
        logging.warning(f"Syntaxe invalide pour {command_name}")
        return "ERROR INVALID_SYNTAX"
    
    try:
        return handler(*parts[1:])
    except Exception as e:
        logging.error(f"Erreur dans le handler : {e}")
        return "ERROR HANDLER_FAILED"


# ============================================================
# GESTION DU CLIENT
# ============================================================

def handle_client(client_socket, client_address):
    """Gère un client"""
    logging.info(f"Nouveau client : {client_address[0]}:{client_address[1]}")
    
    client_socket.settimeout(CLIENT_TIMEOUT)
    command_count = 0
    
    try:
        while True:
            if command_count >= MAX_COMMANDS:
                logging.warning(f"Limite atteinte : {MAX_COMMANDS} commandes")
                send_response(client_socket, "ERROR MAX_COMMANDS_REACHED")
                break
            
            command = receive_command(client_socket)
            if command is None:
                break
            
            logging.info(f"Commande reçue : {command}")
            command_count += 1
            
            response = process_command(command)
            send_response(client_socket, response)
            
    except socket.timeout:
        logging.warning("Timeout client")
        send_response(client_socket, "ERROR TIMEOUT")
    except Exception as e:
        logging.error(f"Erreur avec le client : {e}")
        send_response(client_socket, "ERROR SERVER_ERROR")
    finally:
        client_socket.close()
        logging.info(f"Client déconnecté ({command_count} commandes exécutées)")


# ============================================================
# SERVEUR PRINCIPAL
# ============================================================

def run_server():
    """Lance le serveur"""
    logging.info("Démarrage du serveur")
    
    db_connection = get_db_connection()
    if db_connection is None:
        logging.critical("Impossible de démarrer sans connexion à la BD")
        return
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind((SERVER_IP, SERVER_PORT))
        except OSError as e:
            logging.critical(f"Port {SERVER_PORT} déjà utilisé : {e}")
            return
        
        server.listen(0)
        
        logging.info(f"Serveur démarré sur {SERVER_IP}:{SERVER_PORT}")
        logging.info(f"Timeout : {CLIENT_TIMEOUT}s | Max commandes : {MAX_COMMANDS}")
        logging.info("En attente de connexion...")
        
        while True:
            client_socket, client_address = server.accept()
            handle_client(client_socket, client_address)
            logging.info("Prêt pour un nouveau client")
    
    except KeyboardInterrupt:
        logging.info("Arrêt demandé (Ctrl+C)")
    except Exception as e:
        logging.critical(f"Erreur fatale : {e}")
    finally:
        db_connection.close()
        server.close()
        logging.info("Serveur arrêté")


if __name__ == "__main__":
    run_server()