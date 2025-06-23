#include <stdio.h>
#include <string.h>

void func() {
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
if (4) {
    printf("two");
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
    return 0;
}