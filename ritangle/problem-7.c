#include <stdlib.h>
#include <stdio.h>
#include <math.h>

// CLUE 701

/*
 * Ok so lets get the function that i have to find the min of.
 * Let the function \alpha(H, k) map to the angle between the hour and minute hand.
 * Let the function \beta(H, k) map to the angle between the minute and second hand.
 * Let the function \gamma(H, k) map to the the angle between the hour and second hand.
 *
 * min = h + k
 * sec = h + 2k
 *
 * These should be between 0 and 360
     * \alpha_{sec} = \frac{sec}{60} * 360
     *              = 6*sec
     *              = 6H + 12K
     *
     * \alpha_{min} = \frac{min}{60} * 360 + \frac{alpha_{sec}}{60}
     *              = 6 * min + \frac{6*sec}{60}
     *              = 6 * min + \frac{sec}{10}
     *              = 6H + 6k + \frac{H}{10} + \frac{k}{5}
     *              = \frac{61H}{10} + \frac{31k}{5}
     *
     * \alpha_{hour} = \frac{hour}{12} * 360 + \frac{alpha_{min}}{12}
     *               = 30H + \frac{61H}{120} + \frac{31k}{60}
     *               = \frac{3661H}{120} + \frac{31k}{60}
 *
 * 
 * \alpha = | \alpha_{hour} - \alpha_{min} |
 *        = | \frac{2929H}{120} - \frac{341k}{60} |
 *
 * \beta  = | \alpha_{min} - alpha_{sec} |
 *        = | \frac{H}{10} - \frac{29k}{5} |
 *
 * \gamma = | \alpha_{hour} - \alpha_{sec} |
 *        = | \frac{2941H}{120} - \frac{689k}{60} |
 */

double alpha_angle(int h, int k);
double beta_angle(int h, int k);
double gamma_angle(int h, int k);

int main(){
    double min = 180 * 3;
    int min_h, min_k;
    double min_alpha, min_beta, min_gamma;

    for (int h=0; h<=24; h++){
        for (int k=-60; k<=60; k++){
            if (k != 0){
                double alpha = alpha_angle(h, k);
                double beta = beta_angle(h, k);
                double gamma = gamma_angle(h, k);
                double sum = alpha + beta + gamma;
                if (sum < min & alpha!=-1 & beta!=-1 & gamma != -1){
                    min = sum;
                    min_h = h;
                    min_k = k;

                    min_alpha = alpha;
                    min_beta = beta;
                    min_gamma = gamma;
                }
            }
        }
    }

    printf("Min: %f, Min Hour: %d, Min K: %d\n", min, min_h, min_k);
    printf("Alpha: %f, Beta: %f, Gamma: %f \n", min_alpha, min_beta, min_gamma);
    printf("Alpha + Beta + Gamma = %f\n", min_alpha+min_beta+min_gamma);
}

/*
 * sec = h + 2k
 * min = h + k
 *
 * \alpha_{sec} = \frac{sec}{60} * 360
 *              = 6*sec
 *              = 6H + 12K
 *
 * \alpha_{min} = \frac{min}{60} * 360 + \frac{alpha_{sec}}{60}
 *              = 6 * min + \frac{6*sec}{60}
 *              = 6 * min + \frac{sec}{10}
 *              = 6H + 6k + \frac{H}{10} + \frac{k}{5}
 *              = \frac{61H}{10} + \frac{31k}{5}
 *
 * \alpha_{hour} = \frac{hour}{12} * 360 + \frac{alpha_{min}}{12}
 *               = 30H + \frac{61H}{120} + \frac{31k}{60}
 *               = \frac{3661H}{120} + \frac{31k}{60}
 *
 * \alpha = | \alpha_{hour} - \alpha_{min} |
 *        = | \frac{2929H}{120} - \frac{341k}{60} |
 *
 * \beta  = | \alpha_{min} - alpha_{sec} |
 *        = | \frac{H}{10} - \frac{29k}{5} |
 *
 * \gamma = | \alpha_{hour} - \alpha_{sec} |
 *        = | \frac{2941H}{120} - \frac{689k}{60} |
 */
double alpha_angle(int h, int k){
    if (h + k >= 60 || h+k < 0) return -1;

    double angle = fmod(fabs((2929.0*h)/120.0 - (341.0*k)/60.0 ), 360.0);

    if (angle > 180){
        return 360.0 - angle;
    }
    return  angle;
}

double beta_angle(int h, int k){
    if (h + 2*k >= 60 || h + 2*k < 0) return -1;

    double angle = fmod(fabs( h/10.0 - (29.0*k)/5.0 ), 360.0);

    if (angle > 180){
        return 360.0 - angle;
    }
    return  angle;
}

double gamma_angle(int h, int k){
    if (h + 2*k >= 60 || h + 2*k < 0) return -1;

    double angle = fmod( fabs( (2941.0*h)/120.0 - (689.0*k)/60.0 ), 360.0);

    if (angle > 180){
        return 360.0 - angle;
    }
    return  angle;
}
