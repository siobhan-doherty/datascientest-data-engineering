public class DataScientest extends Student {
    private String specialty;

    public DataScientest(String mail, String specialty, boolean isBootcamp) {
        super(mail, isBootcamp);
        this.specialty = specialty;
    }

    public String getSpecialty() { return specialty; }

    @Override
    public String toString() {
        String res = super.toString();
        res += "\nThe Student is a DataScientest" + specialty;
        return res;
    }
}
