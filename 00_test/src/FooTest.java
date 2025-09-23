class Foo {
    int num;
}

public class FooTest {
    public static void main(String[] args) {
        Foo a = new Foo();
        Foo b = new Foo();
        Foo c = a;
        int A = 1;
        byte B = 1;
        float C = 1;

        System.out.println("========== First TEST ==========");
        if(a == b) System.out.println("a == b");
        if(a == c) System.out.println("a == c");
        if(b == c) System.out.println("b == c");

        a.num = 1;
        c.num = 2;
        System.out.println("a.num = " + a.num + ".");

        System.out.println("========== Second TEST ==========");
        if(A == B) System.out.println("A == B");
        if(A == C) System.out.println("A == C");
        if(B == C) System.out.println("B == C");
    }
}
