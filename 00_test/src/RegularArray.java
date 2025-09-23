import java.util.Arrays;

public class RegularArray {
    public static void main(String[] args) {
        /* 
        int num = 10;
        String[] regularArray = new String[num];
        regularArray[0] = "You are right.";
        regularArray[1] = "You are right.";
        regularArray[2] = "You are right.";
        regularArray[3] = "You are right.";

        for(String line: regularArray){
            System.out.println(line);
        }
        */
        int num = 10;
        int[] regularArray = new int[num];
        for(int i = 0; i < regularArray.length; i++){
            regularArray[i] = (int)(Math.random() * 100);
        }Arrays.sort(regularArray);
        System.out.print("regualrArray = [");
        for(int i: regularArray){
            System.out.print(i + " ");
        }System.out.println("]\n");
        System.out.println(Arrays.toString(regularArray));


        int key = regularArray[num / 2];
        System.out.println("key = " + String.valueOf(key));
        System.out.println("regularArray[num / 2] = " + String.valueOf(regularArray[num / 2]));
        int index = Arrays.binarySearch(regularArray, key);
        System.out.println("ans = " + String.valueOf(regularArray[index]));

        int[] copiedArray = Arrays.copyOf(regularArray, regularArray.length);
        boolean isEqual = Arrays.equals(regularArray, copiedArray);
        System.out.println("isEqual = " + isEqual);
    }
}
