#include <stdio.h>
#include <string.h>
#include <math.h>

int sum(int a, int b) {
    return a+b;
}
int fact(int n) {
    if (n == 0) {
        return 1;
    }
    return n * fact(n - 1);
}
int factorial(int n) {
    if (n == 0 || n == 1) {
        return 1;
    }
    else {
        return n * factorial(n - 1);
}
}

int main() {
int num1;
printf("enter num");
scanf("%d", &num1);
int num2;
printf("enter num:");
scanf("%d", &num2);
int sum1 = sum(num1,num2);
printf("%d\n", sum1);
sqrt(40);
int d = ceil(34);
floor(34);
min(4,3);
int arr[] = {1,2,3,4};
float le[] = {1.2,3.4};
char* huur[] = {"34","44"};
char* rr[] = {"d"};
// Example usage
printf("%d\n", factorial(5));
    return 0;
}