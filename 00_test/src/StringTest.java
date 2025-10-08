public class StringTest {
    String s1 = "Hello";
    String s2 = "World";
    int times = 10;

    public static void main(String[] args) {
        StringTest test = new StringTest();
        System.out.println("s1: " + test.s1);
        System.out.println("s2: " + test.s2);
        System.out.println("");

        // String.format()
        System.out.println("String.format() Test: ");
        String sf = String.format("%s %s for %d times!", test.s1, test.s2, test.times);
        System.out.println(sf);
        System.out.println("");

        // String.charAt()
        System.out.println("String.charAt() Test: ");
        char c1 = test.s1.charAt(0);
        System.out.println("s1[0]: " + c1);
        char c2 = sf.charAt(5);
        System.out.println("sf[5]: " + c2);
        char c3 = sf.charAt(16);
        System.out.println("sf[16]: " + c3);
        System.out.println("");

        // String.substring()
        System.out.println("String.substring() Test: ");
        String ssub1 = sf.substring(3);
        System.out.println("sf[3]: " + ssub1);
        String ssub2 = sf.substring(1, 2);
        System.out.println("sf[1, 2]: " + ssub2);
        System.out.println("");

        // String.trim()
        System.out.println("String.trim() Test: ");
        String st = sf.trim();
        System.out.println("sf.trim(): " + st);
        System.out.println("");

    }
}
