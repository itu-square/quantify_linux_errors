#include<stdio.h>

int func(){}


int main(void) {
    int n;
    int b;
    #ifdef A
        n = 10;
    #endif
    b = func();
    printf("%d", b);
    return 0;
}
