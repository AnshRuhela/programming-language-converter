#include <iostream>
#include <string>
#include <cmath>
#include <vector>
using namespace std;

int fact(int n) {
    if (n == 0) {
        return 1;
    }
    return n * fact(n - 1);
}
int factorial(int n) {
    if (n == 0 or n == 1) {
        return 1;
    }
    else {
        return n * factorial(n - 1);
}
}
void func(int a, int b, int c) {
    cout << "helo" << endl;
}
void func2() {
    for (int i = 0; i < 30; i++) {
        cout << "hl" << endl;
}
}
void func3() {
    cout << "hlo" << endl;
    for (int i = 0; i < 300; i++) {
        cout << "hl" << endl;
    }
    cout << "4" << endl;
}
int func4() {
    cout << "this is fun" << endl;
    return 1;
}

int main() {
cout << "hlo" << endl;
string name;
cout << "enter name: ";
getline(cin, name);
int age;
cout << "enter age: ";
cin >> age;
int a = 30;
int b = 30;
float cc = 3.4;
int rr = 3;
float nn;
cout << "enter number: ";
cin >> nn;
cout << nn << endl;
int x = 0;
while (x < 3) {
    cout << x << endl;
    // x += 1
}
if (4) {
    cout << "two ram ram ram ram" << endl;
}
for (int i = 0; i < 30; i++) {
    cout << "tone" << endl;
}
for (int i = 0; i < 43; i++) {
    if (3) {
        cout << "hle" << endl;
    }
    else if (34) {
        cout << "ee" << endl;
        for (int j = 0; j < 30; j++) {
            cout << 'd' << endl;
}
}
}
for (int i = 0; i < 43; i++) {
    if (3) {
        cout << "hle" << endl;
    }
    else if (34) {
        cout << "ee" << endl;
    }
    else {
        cout << "dfdgj" << endl;
}
}
func2();
func3();
ceil(3.4);
floor(44.4);
pow(3, 4);
int RAM = 0;
RAM=fact(4);
vector<int> arr {1, 2, 3, 4, 5};
vector<string> arr2 {"df"};
vector<float> arr3 {3.4,5.4};
x=min(9,45);
    return 0;
}