#include <stdio.h>
#include <stdlib.h>

int next_permutation(int* int_array, size_t array_size);
void output_int_array(int* int_array, size_t array_size);

int main(){
    int nums[] = {0,1,2,3,4,5};
    size_t num_nums = sizeof(nums)/ sizeof(int);

    do {
        if ((5*(nums[0] + nums[1]) + 9*(nums[2] + nums[3]) + 27*(nums[4] + nums[5])) == 135){
            output_int_array(nums, num_nums);
            break;
        }
    }
    while (next_permutation(nums, num_nums));
    return 0;
}

// the generates the next permutation by finding the next smallest number if they were merged
// like if you were given [1,2,3,4] the next would be [1,2,4,3] then [1,3,2,4] then [1,3,4,2]
// simply put it will swap the last pair of elements where the first element is smaller than the second
int next_permutation(int* int_array, size_t array_size){
    // -2 because otherwise there would be nothing to swap with
    for (int i=array_size-2; i>=0; i--){
        for (int j=array_size-1; j>i; j--){
            if (int_array[i] < int_array[j]){
                // swap i and j elements
                int temp = int_array[i];
                int_array[i] = int_array[j];
                int_array[j] = temp;

                // reverse elements after k
                for (int k=i+1; k<array_size-1; k++){
                    temp = int_array[k];
                    int_array[k] = int_array[array_size - (k - i)];
                    int_array[array_size - (k - i)] = temp;
                }

                // permutation found and changed
                return 1;
            }
        }
    }
    // no next permutation
    return 0;
}

void output_int_array(int* int_array, size_t array_size){
    printf("[");
    for (int i=0; i<array_size; i++){
        if (i < array_size - 1){
            printf("%i, ", int_array[i]);
        }
        else {
            printf("%i", int_array[i]);
        }
    }
    printf("]\n");
}

// CLUE 433
