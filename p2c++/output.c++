#include <iostream>
#include <string>
using namespace std;

void func() {
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
if (4) {
    cout << "two" << endl;
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
    return 0;
}