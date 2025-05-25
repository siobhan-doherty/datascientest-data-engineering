public class Student {
    public static int nbStudent = 0;
    private int id;
    private String mail;
    private boolean isBootcamp;

    public Student(String mail, boolean isBootcamp) {
        this.id = ++nbStudent;
        this.mail = mail;
        this.isBootcamp = isBootcamp;
    }

    public Student() { this(null, false); }

    public int getId() { return id; }
    public String getMail() { return mail; }
    public boolean isBootcamp() { return isBootcamp; }

    @Override
    public String toString() {
        String res = "Student id is " + id + "\n" 
                    + " & student mail is " + mail + "\n";
        res += isBootcamp
            ? "Student is in a Bootcamp"
            : "Student is not in a Bootcamp";
        return res;
    }
}
