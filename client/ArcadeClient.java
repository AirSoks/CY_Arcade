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

    // Les valeurs par défaut pour l'hôte et le port
    private static final String DEFAULT_HOST = "localhost";
    private static final int DEFAULT_PORT = 50001;

    /** 
     * Méthode principale du client arcade.
     * @param args Les arguments de la ligne de commande
     */
    public static void main(String[] args) {
        System.out.println("=== Client Arcade ===");
        help();
        while (true) {
            System.out.print("> ");

            // L'entrée tapé par l'utilisateur
            String input = scanner.nextLine().trim();
            
            if (input.isEmpty()) continue;
            if (input.equalsIgnoreCase("quit")) break;
            
            handleCommand(input);
        }
        
        disconnect();
        scanner.close();
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
                connect(DEFAULT_HOST, DEFAULT_PORT);
                break;
            case "disconnect":
                disconnect();
                break;
            case "read":
                int lines = parts.length > 1 ? Integer.parseInt(parts[1]) : 1;
                read(lines);
                break;
            case "help":
                help();
                break;
            default:
                if (sendCommand(input)) { read(1); }
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
     * Affiche l'aide pour les commandes disponibles.
     */
    private static void help() {
        System.out.println("Commandes disponibles:");
        System.out.println("  connect [host] [port]    - Se connecter au serveur");
        System.out.println("  disconnect               - Se déconnecter");
        System.out.println("  read [nb_lignes]         - Lire la réponse du serveur");
        System.out.println("  quit                     - Quitter");
        System.out.println("  [nb_lignes] <commande>   - Envoyer une commande au serveur\n");
        System.out.println("  help                     - Afficher cette aide");
    }
}