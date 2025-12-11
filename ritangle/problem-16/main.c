#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct digit{
    long double val;
    struct digit* next_digit;
}digit;

int increment_digit(digit* dig, int base);
int main(void){
    digit a= {.val=2, .next_digit=NULL};
    digit b= {.val=2, .next_digit=&a};
    digit c= {.val=2, .next_digit=&b};
    digit d= {.val=2, .next_digit=&c};
    digit e= {.val=2, .next_digit=&d};
    digit f= {.val=2, .next_digit=&e};

    int base = 8;
    long double max = 0;
    long double max_a, max_b, max_c, max_d, max_e, max_f;

    do{
        if (   a.val!=b.val && a.val!=c.val && a.val!=d.val && a.val!=e.val && a.val!=f.val
            && b.val!=c.val&&b.val!=d.val&&b.val!=e.val&&b.val!=f.val
            && c.val!=d.val&&c.val!=e.val&&c.val!=f.val
            && d.val!=e.val&&d.val!=f.val
            && e.val!=f.val
            && c.val/a.val<1 && f.val/d.val<1){

            long double result = a.val / (1- pow(c.val/a.val, 1.0/(b.val-1))) - (d.val / (1 - pow(f.val/d.val, 1.0/(e.val-1))));
            if (result > max){
                max = result;
                printf("%Lf\n", max);
                max_a = a.val;
                max_b = b.val;
                max_c = c.val;
                max_d = d.val;
                max_e = e.val;
                max_f = f.val;
            }
        }
    }
    while (increment_digit(&f, base) != -1);
    printf("MAX: %Lf\n", max);
    printf("a, b, c, d, e, f: %Lf, %Lf, %Lf, %Lf, %Lf, %Lf\n", max_a, max_b, max_c, max_d, max_e, max_f);
}

int increment_digit(digit* dig, int base){
    if (dig->val + 1 >= base){
        if (dig->next_digit != NULL){
            dig->val = 2;
            return increment_digit(dig->next_digit, base);
        }
        return -1;
    }
    dig->val++;
    return 0;
}

