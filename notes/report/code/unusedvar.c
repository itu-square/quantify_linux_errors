#include<stdio.h>

int main(void) {
    int a = 50;
    #ifdef A
    printf("%d", a);
    #endif
    return 0;
}
