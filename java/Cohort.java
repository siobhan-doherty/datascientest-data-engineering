public class Cohort {
    public static int nbCohort = 0;
    public int id;
    public String mail;
    public Student[] arr;

    public int getId() {
        return this.id;
    }

    public String getMail() {
        return this.mail;
    }

    public Student[] getStudents() {
        return this.arr;
    }

    public Cohort(String mail, int size) {
        nbCohort++;
        this.id = nbCohort;
        this.mail = mail;
        this.arr = new Student[size];
    }

    public static void main(String[] args) {
        Cohort DE = new Cohort("director@dst.com", 10);
        System.out.println("Created cohort " + DE.getId() + " directed by " + DE.getMail()
            + " with student " + DE.getStudents().length);
    }
}
