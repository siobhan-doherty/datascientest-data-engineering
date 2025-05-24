public class FirstSteps {
    public static int plus(int a, int b) {
        return a + b;
    }

    public static int plusOne(int a) {
        return plus(a, 1);
    }

    public static void hello(String name) {
        System.out.println("Hello " + name);
    }

    public static int incrementFirstElement(int[] arr) {
        arr[0]++;
        return 1;
    }

    public static String prog(int n) {
        if (n % 2 == 0 && n < 20)
            return "Java";
        else if (n % 2 == 1)
            return "Python";
        else
            return "C";
    }

    // prime helpers
    // isPrime true if n is prime
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i < n; i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
    // nextPrime smallest prime > n
    public static int nextPrime(int n) {
        int p = n + 1;
        while (!isPrime(p)) p++;
        return p;
    }
    // decompose prints prime factorisation
    public static void decompose(int n) {
        int p = n;
        System.out.println(n +" = ");
        for (int i = 2; i < n; i = nextPrime(i)) {
            p = n;
            while (p % i == 0) {
                System.out.println(i + " x ");
                p /= i;
            }
        }
        System.out.println("1");
        if (isPrime(n))
            System.out.println(" x " + n);
    }

    public static void main(String[] args) {
        int a = 1;
        System.out.println(a);
        a = 2;
        System.out.println(a);

        // arithmetic
        int x = 7, y = 3;
        System.out.println(x + y);
        System.out.println(x - y);
        System.out.println(x * y);
        System.out.println(x / y);
        System.out.println(x % y);
        x++;
        System.out.println(x);
        y--;
        System.out.println(y);
        
        // assignment
        int z = 5;
        z += 2;
        System.out.println(z);
        z *= 3;
        System.out.println(z);

        // comparison / logical
        System.out.println(x == y);
        System.out.println(x > y && x < 10);
        System.out.println(x < y || y > 10);
        System.out.println(!(x == y));
        
        // arrays
        int[] tab = {1, 2, 3, 4};
        System.out.println("tab[0]" + tab[0]);
        int[] tab_two = new int[3];
        tab_two[0] = 10;
        tab_two[1] = 20;
        tab_two[2] = 30;
        System.out.println("tab_two[1]:" + tab_two[1]);
        int[][] matrix_one = {{1, 2, 3}, {4, 5, 6}};
        System.out.println("matrix_one[0][2]:" + matrix_one[0][2]);
        int[][] matrix_two = new int[2][3];
        System.out.println("matrix_two[1][1]:" + matrix_two[1][1]);

        // functions
        int result_one = plus(2, 8);
        System.out.println("plus(2, 8): " + result_one);
        int result_two = plusOne(2);
        System.out.println("plusOne(2): " + result_two);
        hello("DataScientest");
        int[] arr = {45, 42, 48};
        System.out.println(arr[0]);
        incrementFirstElement(arr);
        System.out.println(arr[0]);
        if (args.length >= 2) {
           System.out.println("Hello " + args[0] + " " + args[1]);
        }

        // conditions
        for (int num: new int[]{1,2,3,4,5}) {
            System.out.println(num + "->" + prog(num));
        }

        String l = "English";
        switch(l) {
            case "French":
                System.out.println("Salut");
                break;
            case "English":
                System.out.println("Hi");
                break;
            case "German":
                System.out.println("Hallo");
                break;
            case "Spanish":
                System.out.println("Hola");
                break;
            default:
                System.out.println("Not a language");
                break;
        }

        // loops
        // while loop
        int countdown = 10;
        while (countdown != 0) {
            System.out.println(countdown + " ");
            countdown--;
        }
        System.out.println();

        // do while loop
        int dw = -1;
        do {
            System.out.println("do-while outputs: " + dw);
            dw--;
        } while (dw > 0);


        // for loop
        for (int j = 0; j < 10; j++) {
            System.out.println(j + " ");
        }
        System.out.println();
        // Display even numbers from -20 to 20 :
        for (int k = -20; k < 21; k += 2) {
            System.out.println(k + " ");
        }
        System.out.println();
        // enhance for each loop
        int[] sample = {1, 2, 3, 4};
        for(int v : sample){
            System.out.println(v + " ");
        }
        System.out.println();
        // prime tests
        System.out.println("17 prime? " + isPrime(17));
        System.out.println("Next prime > 17 is " + nextPrime(17));
        decompose(84);
    }
}
