import java.io.*;
import java.net.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

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
    
    // Fichier de log
    private static final String LOG_FILE = "client/client.log";
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    public SocketConnexion(String host, int port) {
        this.host = host;
        this.port = port;
    }

    /** 
     * Connecte la classe au serveur.
     * @throws IOException Si une erreur d'E/S se produit
     */
    public void connect() throws IOException {
        socket = new Socket();
        
        // Timeout de connexion : 10 secondes
        socket.connect(new InetSocketAddress(host, port), 10000);
        
        // Timeout de lecture : 30 secondes
        socket.setSoTimeout(30000);
        
        in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        out = new PrintWriter(socket.getOutputStream(), true);
        
        log("CONNEXION établie vers " + host + ":" + port);
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
        log("ENVOI: " + command);
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
        log("REÇU: " + line);
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
            log("DÉCONNEXION de " + host + ":" + port);
            socket.close();
        }
    }
    
    /**
     * Écrit un message dans le fichier de log.
     * @param message Le message à logger
     */
    private void log(String message) {
        try (FileWriter fw = new FileWriter(LOG_FILE, true);
             BufferedWriter bw = new BufferedWriter(fw);
             PrintWriter pw = new PrintWriter(bw)) {
            
            String timestamp = LocalDateTime.now().format(DATE_FORMAT);
            pw.println("[" + timestamp + "] " + message);
            
        } catch (IOException e) {
            System.err.println("Erreur d'écriture dans le log: " + e.getMessage());
        }
    }
}
