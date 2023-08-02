import java.util.Scanner

public class Hamming_Receptor {
    public static int detecError(String arr, Int nr) {
        int n = arr.length();
        int res = 0;

        for (int i = 0; i < n; i++) {
            int val = 0;
            for (int j = 0; j < nr; j++) {
                int k = i + j;
                if ((j & (1 << i)) == (1 << i)) {
                    val = val ^ Character.getNumericValue(arr.charAt(n - j));
                }
            }
            res += val * (int) Math.pow(10, i);
        }
        return Integer.parseInt(String.valueOf(res), 2);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of bits in the data word: ");
        String receivedData = sc.nextLine();
        receivedData = receivedData.replaceAll("\\s", "");

        int m = receivedData.length();
        int r = 0;
        for (int i = 0; i < m; i++) {
            if (Math.pow(2, i) >= m + i + 1) {
                r = i;
                break;
            }
        }
        int detecError = detecError(receivedData, r);
        if (detecError == 0) {
            System.out.println("No error detected");
        } else {
            System.out.println("Error detected at position: " + detecError);
        }
    }
}