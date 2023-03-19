#include <stdio.h>
#include <math.h>
#define DOT "*"
#define VOID "."


void print_result();

int main() {
    print_result();
    return 0;
}

void print_result(){
    double const rows = 25, cols = 80;
    double const x_min = 0, x_max = 4 * M_PI;
    double const y_min = -1, y_max = 1;
    double const step_x = (x_max - x_min) / (cols - 1);

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            double x = x_min + j * step_x;
            double y = sin(cos(2 * x));
            if (i == round((rows - 1) * (y - y_min) / (y_max - y_min))) {
                printf(DOT);
            } else {
                printf(VOID);
            }
        }
        if (i < (rows - 1))
            printf("\n");
    }
}
