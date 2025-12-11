#include <stdlib.h>
#include <stdio.h>

typedef struct {
    int hour, minute, second;
} Stopwatch;

bool increment_stopwatch(Stopwatch* sw);
bool two_unique_digits(Stopwatch* sw);
int main(void){
    int count = 0;
    Stopwatch sw = {.hour=0, .minute=0, .second=0};
    do {
        if (two_unique_digits(&sw)){
            count++;
        }
    }
    while (increment_stopwatch(&sw));

    printf("Total count: %d\n", count);
    return 0;
}

bool increment_stopwatch(Stopwatch* sw){
    if ((sw->second + 1) < 60){
        sw->second++;
        return true;
    }
    else if ((sw->minute + 1) < 60){
        sw->second = 0;
        sw->minute++;
        return true;
    }
    else if ((sw->hour + 1) < 100){
        sw->hour++;
        sw->second = 0;
        sw->minute = 0;
        return true;
    }
    return false;
}

bool two_unique_digits(Stopwatch* sw){
    bool digits[] = {0,0,0,0,0,0,0,0,0,0};
    digits[sw->hour/10] = true;
    digits[sw->hour%10] = true;
    digits[sw->minute/10] = true;
    digits[sw->minute%10] = true;
    digits[sw->second/10] = true;
    digits[sw->second%10] = true;

    int unique_digits = 0;
    for (int i=0; i<10; i++){
        unique_digits += digits[i];
    }
//    if (unique_digits == 2){
//        printf("Second: %d\n", sw->second);
//        printf("Minute: %d\n", sw->minute);
//        printf("Hour: %d\n", sw->hour);
//    }
    return unique_digits == 2;
}
