import java.io.*;
import java.net.*;

/** 
 * Une SocketConnexion représente une connexion à un serveur.
 * C'est une connexion TCP côté client qui permet d'envoyer des commandes
 * et de lire les réponses du serveur.
 */
public class SocketConnexion {
    private final String host;
    private final int port;
    private Socket socket;
    private BufferedReader in;
    private PrintWriter out;
    
    public SocketConnexion(String host, int port) {
        this.host = host;
        this.port = port;
    }

    /** 
     * Connecte la classe au serveur.
     * @throws IOException Si une erreur d'E/S se produit
     */
    public void connect() throws IOException {
        socket = new Socket(host, port);

        // Initialisation des flux d'entrée et de sortie
        in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        out = new PrintWriter(socket.getOutputStream(), true);
    }

    /** 
     * Envoie une commande au serveur.
     * @param command La commande à envoyer
     * @throws IOException Si une erreur d'E/S se produit
     */
    public void sendCommand(String command) throws IOException {
        if (socket == null || socket.isClosed()) {
            throw new IOException("Non connecté au serveur");
        }
        out.println(command);
    }

    /** 
     * Lit une ligne de la réponse du serveur.
     * @return String La ligne lue
     * @throws IOException Si une erreur d'E/S se produit
     */
    public String readLine() throws IOException {
        if (socket == null || socket.isClosed()) {
            throw new IOException("Non connecté au serveur");
        }
        String line = in.readLine();
        if (line == null) {
            throw new IOException("Connexion fermée par le serveur");
        }
        return line;
    }

    /** 
     * Lit plusieurs lignes de la réponse du serveur.
     * @param count Le nombre de lignes à lire
     * @return String Les lignes lues
     * @throws IOException Si une erreur d'E/S se produit
     */
    public String readLines(int count) throws IOException {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < count; i++) {
            if (i > 0) sb.append("\n");
            sb.append(readLine());
        }
        return sb.toString();
    }

    /** 
     * Déconnecte la classe du serveur.
     * @throws IOException Si une erreur d'E/S se produit
     */
    public void disconnect() throws IOException {
        if (socket != null && !socket.isClosed()) {
            socket.close();
        }
    }
}