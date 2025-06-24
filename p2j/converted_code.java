import java.util.*;

public class Main {
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
// All testing code
// Test comment

int x = 5;

float y = 3.14f;

String name = "Test";

boolean flag = true;

ArrayList<String> items = new ArrayList<>();
items.add("apple");
items.add("banana");

int count = 0;

count += 1;

int n;
System.out.print("Enter a number: ");
n = scanner.nextInt();
scanner.nextLine(); // Clear buffer

float f;
System.out.print("Enter a float: ");
f = scanner.nextFloat();
scanner.nextLine(); // Clear buffer

int s = input("Enter a string: ");

System.out.printf("Number: %d, Float: %.2f, String: %d\n", n, f, s);

System.out.println("Hello, World!");

for (int i = 0; i < 5; i ++) {

        System.out.println(i);

}

for (int j = 2; j < 7; j += 2) {

        if (j == 4) {

                System.out.println("Found 4");

        }

    } else if (j == 6) {

                System.out.println("Found 6");

        }

    } else {

                System.out.println("Other");

        }

}

while (count < 3) {

        System.out.println(count);

        count += 1;

        if (count == 2) {

                continue;

        }

        if (count == 3) {

                break;

        }

}

// TODO: Unhandled: ___________________________________________________

// TODO: Unhandled: Testing for Python to java code....

int num;
System.out.print("Enter a number: ");
num = scanner.nextInt();
scanner.nextLine(); // Clear buffer

int result = factorial(num);

System.out.printf("Factorial of %d is: %d\n", num, result);

// TODO: Unhandled: _________________________________

// NORMAL INPUT TESTING:
// Integer input

int a;
System.out.print("Enter first integer: ");
a = scanner.nextInt();
scanner.nextLine(); // Clear buffer

int b;
System.out.print("Enter second integer: ");
b = scanner.nextInt();
scanner.nextLine(); // Clear buffer

int int_sum = a + b;

// Float input

float x;
System.out.print("Enter first float: ");
x = scanner.nextFloat();
scanner.nextLine(); // Clear buffer

float y;
System.out.print("Enter second float: ");
y = scanner.nextFloat();
scanner.nextLine(); // Clear buffer

int float_sum = x + y;

// String number input

int s1 = input("Enter first string number: ");

int s2 = input("Enter second string number: ");

int string_sum = s1 + s2  # Concatenation;

// Output

System.out.println("\nResults:");

System.out.println("Sum of integers:", int_sum);

System.out.println("Sum of floats:", float_sum);

System.out.println("Concatenated string numbers:", string_sum);

// TODO: Unhandled: _____________________________________________________

// FOR LOOPING TESTING:
// While Loop: Counting from 1 to 5

System.out.println("Using WHILE loop (Counting 1 to 5):");

int i = 1;

while (i <= 5) {

        System.out.println("Number:", i);

        i += 1;

}

// For Loop: Printing square of numbers 1 to 5

System.out.println("\nUsing FOR loop (Squares of 1 to 5):");

for (int j = 1; j < 6; j ++) {

        System.out.println("Square of j is:", j * j);

}

// TODO: Unhandled: _______________________________________

// condition testing :
// Input from user

int num;
System.out.print("Enter a number: ");
num = scanner.nextInt();
scanner.nextLine(); // Clear buffer

// == equal to

if (num == 0) {

        System.out.println("Number is zero (== 0)");

}

// != not equal to

} else if (num != 0) {

        System.out.println("Number is not zero (!= 0)");

        // > greater than

        if (num > 0) {

                System.out.println("Number is positive (> 0)");

                // >= greater than or equal to

                if (num >= 10) {

                        System.out.println("Number is greater than or equal to 10 (>= 10)");

                }

            } else {

                        System.out.println("Number is less than 10 but positive (< 10)");

                }

        }

        // < less than

    } else if (num < 0) {

                System.out.println("Number is negative (< 0)");

                // <= less than or equal to

                if (num <= -10) {

                        System.out.println("Number is less than or equal to -10 (<= -10)");

                }

            } else {

                        System.out.println("Number is greater than -10 but still negative (> -10)");

                }

        }

}

// TODO: Unhandled: ________________________________________-

    }

public static int add_numbers(int a, int b) {

        int result = a + b;

        return result;
}

public static String get_name() {

        return "Alice";
}

public static boolean check_bool() {

        return true;
}

public static ArrayList<String> get_list() {

        ArrayList<String> result = new ArrayList<>();
        result.add("item1");
        result.add("item2");
        return result;

}

public static int factorial(int n) {

        if (n < 0) {

                return 0;
        }

    } else if (n == 0 || n == 1) {

                return 1;
        }

    } else {

                int fact = 1;

                for (int i = 2; i <= n; i ++) {

                        fact *= i;

                }

                return fact;
        }

}

}