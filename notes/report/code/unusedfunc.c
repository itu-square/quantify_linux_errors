#include<stdio.h>

static int __deprecated func() {
    return 100;
}

int main(void) {
    int b;
    b = func();
    printf("%d", b);
    return 0;
}
