#include "data_stat.h"

double max(double *data, int n){
    double current_max = data[0];
    for (int index = 0; index < n; index++) {
        double current_value = data[index];
        if (current_value > current_max) {
            current_max = current_value;
        }
    }
    return current_max;
}

double min(double *data, int n) {
    double current_min = data[0];
    for (int index = 0; index < n; index++) {
        double current_value = data[index];
        if (current_value < current_min) {
            current_min = current_value;
        }
    }
    return current_min;
}

double mean(double *data, int n) {
    double current_mean = 0;
    for (int index = 0; index < n; index++) {
        double current_value = data[index];
        current_mean += (current_value - current_mean) / (index+1);
    }
    return current_mean;
}

double variance(double *data, int n) {
    double mean_value = mean(data, n);
    double current_variance = 0.0;
    for (int index = 0; index < n; index++) {
        double variance_update = (data[index] - mean_value);
        current_variance += variance_update*variance_update / n;
    }
    return current_variance;
}
