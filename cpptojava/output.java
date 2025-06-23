import java.util.*;
public class Main {
    public static int sumArray(int arr, int n) {
        int sum = 0;
        for (int i = 0; i < n; i++) {;
        sum += arr[i];
        cout << arr[i] << " ";
    }
        return sum;
    }
    public static int multiply(int arr, int n) {
        if(n < 2);
        return arr[i];
        return arr[n-1] * multiply(arr , n-1);
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n;
        n = sc.nextInt();
        int[] arr = new int[100];
        for (int i = 0; i < n; i++) {
        arr[i] = sc.next();
        }
        int total = sumArray(arr, n);
        System.out.print("Total: " + String.valueOf(total) + "\n");
        int multi = multiply(arr,n);
        System.out.print("Multiply: " + String.valueOf(multi) + "\n");
    }
        }