#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct e_p_combo {
    int even;
    int prime;
} e_p_combo;

bool check_e_p_combo(e_p_combo combo);

int main(void){
    int primes[] = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,91,97};

    int num_primes = 25;
    int num_evens = 49;
    int num_combos = num_primes * num_evens;

    e_p_combo all_e_p_combos[num_primes * num_evens];
    for (int i=0; i<num_combos; i++){
        // it will start with the first prime and go through all the evens, then the second prime...
        all_e_p_combos[i] = (e_p_combo){.prime=primes[i/num_evens],.even=2*((i%num_evens)+1)};
        // printf("%d, %d, %d\n",i/num_evens , all_e_p_combos[i].prime, all_e_p_combos[i].even);
    }

    int success = 0;
    int total = 0;
    for (int i=0; i<num_combos; i++){
        total++;
        if (check_e_p_combo(all_e_p_combos[i])){
            success++;
        }
    }
    printf("%d, %d \n%f\n", success, total, (float)success/total);

    return 0;
}

bool check_e_p_combo(e_p_combo combo){
    /*
     * so here i am check if ax+b = cx+d has an integer x answer.
     * In this case it is Ex+P = -Px + 1000E
     * So x = (1000E-P)/(E+P)
     */
    if (fmod((1000.0*combo.even - combo.prime) / (combo.even + combo.prime), 1.0) == 0){
        return true;
    }
    return false;
}
