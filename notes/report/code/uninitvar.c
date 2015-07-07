#include<stdio.h>

int main(void) {
    int a;
    #ifdef A
        a = 10;
    #endif
    printf("%d", a);
    return 0;
}
