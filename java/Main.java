public class Main {
    public static void main(String[] args) {
        DataEngineer diane  = new DataEngineer("diane@dst.com", "172-31-18-113", false);
        Student donna = new Student("donna@dst.com", true);
        DataScientest nicole = new DataScientest("nicole@dst.com", "Manager", true);
        System.out.println(diane);
        System.out.println();
        System.out.println(donna);
        System.out.println();
        System.out.println(nicole);
    }
}
