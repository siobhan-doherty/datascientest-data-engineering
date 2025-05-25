import java.util.ArrayList;


public class Array {
    public static void main(String[] args) {
        ArrayList<Integer> listInteger = new ArrayList<Integer>();
        ArrayList<String> listString = new ArrayList<String>();
        ArrayList<Student> cohort = new ArrayList<Student>();

        int[] arr = {1, 2, 3};
        for (int i = 0; i < arr.length; i++) {
            listInteger.add(arr[i]);
            listString.add("v" + arr[i]);
            cohort.add(new Student("s" + arr[i], true));
        }

        for(Integer x: listInteger) System.out.println(x);
        for(String s: listString) System.out.println(s);
        for(Student st: cohort) System.out.println(st);
    }
}
