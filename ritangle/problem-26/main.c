#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*
 * this is a EXTREMELY innefficient method
 */

int int_in_array(int int_to_be_found, int* int_array, int num_elements);
int hcf_calc(int a, int b);
int next_permutation(int* int_array, size_t array_size);

int main(void){
    int nums[] = {1,2,3,4,5,6,7,8,9,10};
    int all_hcf[10000];
    int num_hcf = 0;
    do{
        int a = nums[0]*nums[1]*nums[2]*nums[3]*nums[4];
        int b = nums[5]*nums[6]*nums[7]*nums[8]*nums[9];
        int hcf = hcf_calc(a, b);
        if (!int_in_array(hcf, all_hcf, num_hcf)){
            all_hcf[num_hcf] = hcf;
            num_hcf++;
        }
    }
    while (next_permutation(nums, 10) != -1);

    int sum = 0;
    for (int i=0; i<num_hcf; i++){
        sum += all_hcf[i];
    }
    printf("%d\n", sum);

    return 0;
}

int hcf_calc(int a, int b){
    int hcf;
    for(int i = 1; i <= a || i <= b; i++) {
        if( a%i == 0 && b%i == 0 )
            hcf = i;
    }
    return hcf;
}
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
                return 0;
            }
        }
    }
    // no next permutation
    return -1;
}

int int_in_array(int int_to_be_found, int* int_array, int num_elements){
    for (int i=0; i<num_elements; i++){
        if (int_array[i] == int_to_be_found){
            return 1;
        }
    }
    return 0;
}
