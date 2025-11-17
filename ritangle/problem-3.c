#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    srand(time(NULL));

    int d_roll;
    int total_num_trials = 20000000;
    int num_successes = 0;

    bool is_zero;
    bool is_2_zero;
    bool is_two;
    bool is_five;

    for (int i=0; i<total_num_trials; i++){
        is_zero = false;
        is_2_zero = false;
        is_two = false;
        is_five = false;

        for (int j=0; j<5; j++){
            d_roll = rand() % 6 + 1;
            // If current role is 0
            if (d_roll == 0){
                // if there was previously a zero
                if (is_zero){
                    is_2_zero = true;
                }
                // if there wasn't a previous zero
                else{
                    is_zero = true;
                }
            }

            // if current role is 2
            if (d_roll == 2){
                is_two = true;
            }

            // if current roll is 5
            if (d_roll == 5){
                is_five = true;
            }
        }

        // if there was a 2 and a 5 in the previous roll's
        if (is_2_zero || (is_two && is_five) || (is_five && is_zero)){
            num_successes++;
        }
    }

    printf("Probability: %f\n", (float)num_successes / (float)total_num_trials);

    return 0;
}

// clue is 259
