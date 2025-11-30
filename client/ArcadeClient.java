import java.io.IOException;
import java.util.Scanner;

/** 
 * Classe principale pour le client de la borne d'arcade.
 * Permet de communiquer avec un serveur via la classe SocketConnexion.
 */
public class ArcadeClient {

    // Le scanner pour lire les entrées utilisateur
    private static final Scanner scanner = new Scanner(System.in);

    // Le SocketConnexion pour la communication avec le serveur
    private static SocketConnexion socketConnexion = null;

    // Configuration de la borne
    private static ClientConfig config = null;

    /** 
     * Méthode principale du client arcade.
     * @param args Les arguments de la ligne de commande
     */
    public static void main(String[] args) {
        System.out.println("=== Client Arcade ===");
        
        // Charger la configuration
        try {
            config = ClientConfig.load("client/client.conf");
            System.out.println("Configuration chargée: " + config.getHost() + ":" + config.getPort() + " (Borne ID: " + config.getBorneId() + ")");
        } catch (IOException e) {
            System.err.println("Erreur lors du chargement de la configuration: " + e.getMessage());
            System.exit(1);
        }
        
        // Connexion automatique au démarrage
        connect(config.getHost(), config.getPort());
        
        // Si connecté, initialiser la borne et afficher les jeux disponibles
        if (socketConnexion != null) {
            initializeBorne();
        }
        
        help();
        
        while (true) {
            System.out.print("> ");

            // L'entrée tapée par l'utilisateur
            String input = scanner.nextLine().trim();
            
            if (input.isEmpty()) continue;
            if (input.equalsIgnoreCase("quit")) break;
            
            handleCommand(input);
        }
        
        disconnect();
        scanner.close();
    }

    /**
     * Initialise la borne et affiche les jeux disponibles.
     */
    private static void initializeBorne() {
        try {
            // Envoyer la commande START_BORNE avec l'ID de la borne
            socketConnexion.sendCommand("START_BORNE " + config.getBorneId());
            
            // Lire la réponse du serveur
            String response = socketConnexion.readLine();
            
            // Parser et afficher les jeux disponibles
            if (response.startsWith("OK ")) {
                String jeuxData = response.substring(3).trim();
                displayAvailableGames(jeuxData);
            } else {
                System.err.println("Erreur lors de l'initialisation: " + response);
            }
        } catch (IOException e) {
            System.err.println("Erreur lors de l'initialisation de la borne: " + e.getMessage());
        }
    }

    /**
     * Affiche les jeux disponibles à partir des données reçues.
     * @param jeuxData Les données des jeux
     */
    private static void displayAvailableGames(String jeuxData) {
        System.out.println("\nJeux disponibles :");
        
        if (jeuxData.isEmpty()) {
            System.out.println("  Aucun jeu disponible.");
            return;
        }
        
        String[] jeux = jeuxData.split(",");
        for (String jeu : jeux) {
            String[] parts = jeu.split(":");
            System.out.println("  - " + parts[0] + " " + parts[1]);
        }
        System.out.println();
    }

    /** 
     * Gère les commandes utilisateur.
     * @param input La commande entrée par l'utilisateur
     */
    private static void handleCommand(String input) {
        String[] parts = input.split(" ");
        String cmd = parts[0].toLowerCase();
        switch (cmd) {
            case "connect":
                connect(config.getHost(), config.getPort());
                break;
            case "disconnect":
                disconnect();
                break;
            case "help":
                help();
                break;
            default:
                if (!isValidCommand(input)){
                    System.out.println("La commande ne respecte pas la forme: COMMAND <parametres>.");
                    break;
                }
                if (sendCommand(input)) { 
                    read(1); 
                }
        }
    }

    /** 
     * Connecte au serveur.
     * @param host L'hôte du serveur
     * @param port Le port du serveur
     */
    private static void connect(String host, int port) {
        try {
            if (socketConnexion != null) {
                socketConnexion.disconnect();
            }
            socketConnexion = new SocketConnexion(host, port);
            socketConnexion.connect();
            System.out.println("Connecté à " + host + ":" + port);
        } catch (IOException e) {
            System.err.println("Erreur de connexion: " + e.getMessage());
            socketConnexion = null;
        }
    }

    /** 
     * Déconnecte du serveur.
     */
    private static void disconnect() {
        if (socketConnexion == null) {
            System.out.println("Non connecté.");
            return;
        }
        
        try {
            socketConnexion.disconnect();
            System.out.println("Déconnecté.");
        } catch (IOException e) {
            System.err.println("Erreur lors de la déconnexion: " + e.getMessage());
        } finally {
            socketConnexion = null;
        }
    }

    /** 
     * Envoie une commande au serveur.
     * @param command La commande à envoyer
     * @return Boolean Succès de l'envoi
     */
    private static Boolean sendCommand(String command) {
        if (socketConnexion == null) {
            System.out.println("Non connecté. Tapez 'connect' d'abord.");
            return false;
        }
        try {
            socketConnexion.sendCommand(command);
            return true;
        } catch (IOException e) {
            System.err.println("Erreur d'envoi: " + e.getMessage());
            socketConnexion = null;
            return false;
        }
    }

    /** 
     * Lire la réponse du serveur.
     * @param nbLines Le nombre de lignes à lire
     */
    private static void read(int nbLines) {
        if (socketConnexion == null) {
            System.out.println("Non connecté.");
            return;
        }
        try {
            if (nbLines == 1) {
                String line = socketConnexion.readLine();
                System.out.println(line);
            } else {
                String lines = socketConnexion.readLines(nbLines);
                System.out.println(lines);
            }
        } catch (IOException e) {
            System.err.println("Erreur de lecture: " + e.getMessage());
            disconnect();
        }
    }

    /** 
     * Vérifie la structure de la commande selon ce format :
     * COMMAND <parametres>
     * @param command La commande à vérifier
     * @return Boolean Succès de la validation
     */
    private static Boolean isValidCommand(String command) {
        if (command == null) {
            return false;
        }

        String regex = "^[A-Z_]+(?:[ ][1-9][0-9]*)+$";
        return command.trim().matches(regex);
    }


    /** 
     * Affiche l'aide pour les commandes disponibles.
     */
    private static void help() {
        System.out.println("Commandes disponibles:");
        System.out.println("  connect                - Se connecter au serveur");
        System.out.println("  disconnect             - Se déconnecter");
        System.out.println("  COMMAND <parametres>   - Se déconnecter");
        System.out.println("  quit                   - Quitter");
        System.out.println("  help                   - Afficher cette aide");
    }
}
