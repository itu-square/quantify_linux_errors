#include<stdio.h>

int main(void) {
    int var;
    #ifdef CONFIG_A
    var = 1;
    #endif
    #ifdef CONFIG_B
    var = 2;
    #endif
return var+100;
}
