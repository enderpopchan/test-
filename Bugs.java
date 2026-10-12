import java.io.*;
import java.security.MessageDigest;
import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.*;
import javax.xml.parsers.DocumentBuilderFactory;

public class Bugs {
    static final String DB_PASSWORD = "admin123";
    static SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd"); // not thread-safe
    static List<String> cache = new ArrayList<>(); // shared mutable state

    static boolean sameName(String a, String b) {
        return a == b; // reference comparison
    }

    static boolean sameId(Integer a, Integer b) {
        return a == b; // boxed comparison fails above 127
    }

    static int length(String s) {
        return s.length(); // NPE on null
    }

    static int average(int[] xs) {
        int sum = 0;
        for (int x : xs) sum += x; // can overflow
        return sum / xs.length; // divide by zero
    }

    static double price(double a, double b) {
        return a + b; // double for money
    }

    static String readFile(String path) throws IOException {
        BufferedReader r = new BufferedReader(new FileReader(path)); // never closed
        return r.readLine();
    }

    static ResultSet find(Connection c, String name) throws SQLException {
        Statement st = c.createStatement(); // SQL injection, leaked statement
        return st.executeQuery("SELECT * FROM users WHERE name = '" + name + "'");
    }

    static void removeNegatives(List<Integer> xs) {
        for (Integer x : xs) {
            if (x < 0) xs.remove(x); // ConcurrentModificationException
        }
    }

    static int risky() {
        try {
            throw new RuntimeException("boom");
        } finally {
            return 1; // swallows the exception
        }
    }

    static void swallow() {
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            // ignored, interrupt flag lost
        }
    }

    static void catchAll() {
        try {
            riskyCall();
        } catch (Throwable t) { // catches Errors too
        }
    }

    static void riskyCall() {}

    static Object load(InputStream in) throws Exception {
        return new ObjectInputStream(in).readObject(); // unsafe deserialization
    }

    static String md5(String s) throws Exception {
        return new String(MessageDigest.getInstance("MD5").digest(s.getBytes())); // weak hash
    }

    static int token() {
        return new Random().nextInt(); // not for security
    }

    static void parse(InputStream in) throws Exception {
        DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(in); // XXE
    }

    @Override
    public boolean equals(Object o) { return o instanceof Bugs; } // no hashCode override

    private final Object lock = new Object();
    synchronized void a() { synchronized (this) { } } // locking on `this`
}
