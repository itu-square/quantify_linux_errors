#include<stdio.h>

static int  func() {
    int a = 1;
    if (a == 1) return 1;
    if (a == 2) return 0;
}

int main(void) {
    int b;
    b = 9;
    printf("%d", b);
    func();
    return 0;
}
