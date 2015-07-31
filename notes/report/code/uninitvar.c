#include<stdio.h>

int main(void) {
    int n;
    #ifdef A
        n = 10;
    #endif
    printf("%d", n);
    return 0;
}
