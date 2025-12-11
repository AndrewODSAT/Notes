#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct digit{
    long double val;
    struct digit* next_digit;
}digit;

int increment_digit(digit* dig, int base);
int main(void){
    digit p= {.val=1, .next_digit=NULL};
    digit q= {.val=1, .next_digit=&p};
    digit r= {.val=1, .next_digit=&q};

    int base = 7;
    int attempts = 0;
    int success = 0;

    do{
        int largest, small_sum;
        if (p.val>=q.val && p.val>=r.val){
            largest = p.val;
            small_sum = q.val+r.val;
        }
        else if (q.val>=r.val && q.val>=p.val){
            largest = q.val;
            small_sum = p.val+r.val;
        }
        else if (r.val>=q.val && r.val>=p.val){
            largest = r.val;
            small_sum = q.val+p.val;
        }
        if (largest > small_sum){
            success++;
        }
        attempts++;
    }
    while (increment_digit(&r, base) != -1);
    printf("Attempts: %i, success: %i, prob: %f\n", attempts, success, success/(float)attempts);
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


