#include <stdio.h>
#include <stdlib.h>
#include "data_process.h"
#include "../data_libs/data_io.h"

int main() {
    int n;
    double *data;

    //Don`t forget to allocate memory !
    input(&data, &n);

    if (normalization(data, n)) {
        output(data, n);
    } else {
        printf("ERROR");
    }
//    free(data);
}
