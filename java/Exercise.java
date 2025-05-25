import java.util.ArrayList;


public class Exercise {
    // InsertionSort returns a new sorted copy of SomeList
    public static ArrayList<Integer> InsertionSort(ArrayList<Integer> SomeList) {
        // clone() returns Object, cast it back to ArrayList<Integer>
        ArrayList<Integer> T = new ArrayList<>(SomeList);

        for (int i = 0; i < T.size(); i++) {
            int x = T.get(i);
            int j = i;
            while (j > 0 && T.get(j-1) > x) {
                T.set(j, T.get(j-1));
                j = j - 1;
            }
            T.set(j, x);
        }

        return T;
    }

    // FindKLargest returns K largest elements of SomeList, in descending order
    public static ArrayList<Integer> FindKLargest(ArrayList<Integer> SomeList, int K) {
        ArrayList<Integer> T = InsertionSort(SomeList);
        ArrayList<Integer> KLargest = new ArrayList<Integer>();

        // take final K elements from sorted list
        for (int i = 1; i <= K; i++) {
            KLargest.add(T.get(T.size() - i));
        }

        return KLargest;
    }

    public static void main(String[] args) {
        // creation of descending list [99,98,97,...,90]
        ArrayList<Integer> listInteger = new ArrayList<Integer>();
        
        for (int i = 0; i < 10; i++) {
            listInteger.add(99 - i);
        }

        System.out.println(listInteger);
        ArrayList<Integer> Sorted = InsertionSort(listInteger);
        System.out.println(Sorted);

        ArrayList<Integer> KLargest = FindKLargest(listInteger, 5);
        System.out.println(KLargest);
    }
}
