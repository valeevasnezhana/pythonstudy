#include <stdio.h>
#include <stdlib.h>
#include "data_io.h"

void input(double **data, int *n) {
    scanf("%d", n);
    *data = (double*)malloc(*n * sizeof(double));
    double current_value = -1.0;
    for (int index = 0; index < *n; index++) {
        scanf("%lf", &current_value);
        (*data)[index] = current_value;
    }
}

void output(double *data, int n) {
    for (int index = 0; index < n; index++) {
        printf("%.2lf", data[index]);
        if (index < n - 1) {
            printf(" ");
        }
    }
}

