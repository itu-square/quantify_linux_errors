#include<stdio.h>

static int func() {
    return 100;
}

int main(void) {
    int b = 50;
    #ifdef A
    b = func();
    #endif
    printf("%d", b);
    return 0;
}
