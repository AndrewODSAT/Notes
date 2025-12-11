#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct digit{
    long double val;
    struct digit* next_digit;
}digit;

int increment_digit(digit* dig, int base);

int main(void){
    digit a= {.val=1, .next_digit=NULL};
    digit b= {.val=1, .next_digit=&a};
    digit c= {.val=1, .next_digit=&b};
    digit d= {.val=1, .next_digit=&c};

    int base = 100;
    int max = 0;
    long double max_a, max_b, max_c, max_d;

    do{
        if (a.val > b.val 
            && a.val!=b.val && a.val!=c.val && a.val!=d.val && b.val!=c.val&&b.val!=d.val&&c.val!=d.val){
            long double result = (sqrtl(a.val) + sqrtl(b.val)) * (sqrtl(c.val) - sqrtl(d.val));
            if (fmodl(result, 1)==0 && result > max){
                max = result;
                printf("%i\n", max);
                max_a = a.val;
                max_b = b.val;
                max_c = c.val;
                max_d = d.val;
            }
        }
    }
    while (increment_digit(&d, base) != -1);
    printf("MAX: %i\n", max);
    printf("a, b, c, d: %Lf, %Lf, %Lf, %Lf\n", max_a, max_b, max_c, max_d);
}

int increment_digit(digit* dig, int base){
    if (dig->val + 1 >= base){
        if (dig->next_digit != NULL){
            dig->val = 1;
            return increment_digit(dig->next_digit, base);
        }
        return -1;
    }
    dig->val++;
    return 0;
}

