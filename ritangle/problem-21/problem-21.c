#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct digit{
    int val;
    struct digit* next_digit;
}digit;

int increment_digit(digit* dig, int base);

int main(void){
    digit a= {.val=0, .next_digit=NULL};
    digit b= {.val=0, .next_digit=&a};
    digit c= {.val=0, .next_digit=&b};
    digit d= {.val=0, .next_digit=&c};

    int base = 50;
    double total = 0;

    do{
        total += (double)1.0 / (pow(2, a.val) * pow(3, b.val) * pow(5, c.val) * pow(7, d.val));
    }
    while (increment_digit(&d, base) != -1);
    printf("Total: %f\n", total);
}

int increment_digit(digit* dig, int base){
    if (dig->val + 1 >= base){
        if (dig->next_digit != NULL){
            dig->val = 0;
            return increment_digit(dig->next_digit, base);
        }
        return -1;
    }
    dig->val++;
    return 0;
}
