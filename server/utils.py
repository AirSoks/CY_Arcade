"""
utils.py – Fonctions utilitaires (config, logging, BD, réseau, validation)
"""

import os
import sys
import logging
import psycopg2
import configparser
import socket

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_CONFIG_FILE = os.path.join(BASE_DIR, 'server.conf')

MIN_ID = 1
MAX_ID = 999999

def load_config(config_file=SERVER_CONFIG_FILE):
    """Charge la configuration du serveur et de la base de données"""
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    return {
        'SERVER_IP': config.get('SERVER', 'HOST', fallback='localhost'),
        'SERVER_PORT': config.getint('SERVER', 'PORT', fallback=50001),
        'CLIENT_TIMEOUT': config.getint('SERVER', 'TIMEOUT'),
        'MAX_COMMANDS': config.getint('SERVER', 'MAX_COMMANDS'),

        'DB_HOST': config.get('DATABASE', 'DB_HOST'),
        'DB_PORT': config.getint('DATABASE', 'DB_PORT'),
        'DB_NAME': config.get('DATABASE', 'DB_NAME'),
        'DB_USER': config.get('DATABASE', 'DB_USER'),
        'DB_PASSWORD': config.get('DATABASE', 'DB_PASSWORD'),

        'LOG_FILE': config.get('LOGGING', 'LOG_FILE')
    }


def setup_logging(log_file):
    """Configure le logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
                                       datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_db_connection(config):
    """Connexion à la base de données"""
    try:
        db_connection = psycopg2.connect(
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            database=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD']
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
        return data.split('\n')[0].strip()
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


def validate_id(value, field_name="ID"):
    """Valide qu'un ID est valide (entier > 0)
    Lève une exception si invalide"""
    try:
        val_int = int(value)
        if val_int < MIN_ID or val_int > MAX_ID:
            raise ValueError(f"ERROR INVALID_{field_name.upper()}")
        return val_int
    except ValueError as e:
        if str(e).startswith("ERROR"):
            raise
        raise ValueError(f"ERROR INVALID_{field_name.upper()}")


def validate_positive_int(value, min_val, max_val, error_msg):
    """Valide qu'une valeur est un entier dans une plage donnée
    Lève une exception si invalide"""
    try:
        val_int = int(value)
        if val_int < min_val or val_int > max_val:
            raise ValueError(error_msg)
        return val_int
    except ValueError as e:
        if str(e).startswith("ERROR"):
            raise
        raise ValueError(error_msg)


def parse_command(command, expected_keyword, expected_params):
    """Parse et valide une commande
    Retourne la liste des parties si valide"""
    if not command:
        raise ValueError(f"ERROR PROTOCOL_VIOLATION Expected {expected_keyword}")
    
    parts = command.strip().split()
    
    if len(parts) == 0 or parts[0] != expected_keyword:
        raise ValueError(f"ERROR PROTOCOL_VIOLATION Expected {expected_keyword}")
    
    if len(parts) != expected_params:
        raise ValueError("ERROR INVALID_SYNTAX")
    
    return parts


def expect_command(client_socket, expected_keyword, expected_parts):
    """Attend et valide une commande"""
    command = receive_command(client_socket)
    return parse_command(command, expected_keyword, expected_parts)


def verify_card_id(parts, expected_id, position=1):
    """Vérifie que l'ID de carte correspond"""
    if parts[position] != expected_id:
        raise ValueError("ERROR PROTOCOL_VIOLATION Wrong card ID")