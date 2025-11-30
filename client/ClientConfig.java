import java.io.*;
import java.util.*;

public class ClientConfig {
    private final String host;
    private final int port;
    private final int borneId;

    private ClientConfig(String host, int port, int borneId) {
        this.host = host;
        this.port = port;
        this.borneId = borneId;
    }

    public static ClientConfig load(String filename) throws IOException {
        Properties props = new Properties();
        try (FileInputStream fis = new FileInputStream(filename)) {
            props.load(fis);
        }

        String host = props.getProperty("host", "localhost");
        int port = Integer.parseInt(props.getProperty("port", "50001"));
        int borneId = Integer.parseInt(props.getProperty("borne_id", "1"));

        return new ClientConfig(host, port, borneId);
    }

    public String getHost() { 
        return host; 
    }

    public int getPort() { 
        return port; 
    }

    public int getBorneId() { 
        return borneId; 
    }
}
