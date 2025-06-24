#include <stdio.h>
#include <string.h>
#include <math.h>

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
void func(int a, int b, int c) {
    printf("helo");
}
void func2() {
    for (int i = 0; i < 30; i += 1) {
        printf("hl");
}
}
void func3() {
    printf("hlo");
    for (int i = 0; i < 300; i += 1) {
        printf("hl");
    }
    printf("4");
}
int func4() {
    printf("this is fun");
    return 1;
}

int main() {
printf("hlo");
char name[100];
printf("enter name: ");
scanf("%s", name);
int age;
printf("enter age: ");
scanf("%d", &age);
int a = 30;
int b = 30;
float cc = 3.4;
int rr = 3;
float nn;
printf("enter number: ");
scanf("%f", &nn);
printf("%f\n", nn);
int x = 0;
while (x < 3) {
    printf("%d\n", x);
    x += 1;
}
if (4) {
    printf("two ram ram ram ram");
}
for (int i = 0; i < 30; i += 1) {
    printf("tone");
}
for (int i = 0; i < 43; i += 1) {
    if (3) {
        printf("hle");
    }
    else if (34) {
        printf("ee");
        for (int j = 0; j < 30; j += 1) {
            printf('d');
}
}
}
for (int i = 0; i < 43; i += 1) {
    if (3) {
        printf("hle");
    }
    else if (34) {
        printf("ee");
    }
    else {
        printf("dfdgj");
}
}
func2();
func3();
ceil(3.4);
floor(44.4);
pow(3, 4);
int RAM = 0;
int RAM = fact(4);
int arr[] = {1, 2, 3, 4, 5};
char* arr2[] = {"df"};
float arr3[] = {3.4,5.4};
int x = min(9,45);
    return 0;
}