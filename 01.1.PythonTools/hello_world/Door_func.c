#include <math.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    double begin_x = -M_PI;
    double end_x = M_PI;
    double step_x = (end_x - begin_x) / 41;
    double epsilon = 1e-10;
    int iteration = 0;
    for (double current_x = begin_x; current_x <= (end_x + epsilon); current_x += step_x) {
        double chosen_x;
        if (iteration == 41) {
            chosen_x = end_x;
        } else {
            chosen_x = current_x;
        }

        printf("%.7lf", chosen_x);
        printf(" | ");

        double va_value = 1 / (1 + pow(chosen_x, 2));
        printf("%.7lf", va_value);
        printf(" | ");

        double lb_left_value = sqrt(1 + 4 * pow(chosen_x, 2));
        double lb_value_under_sqr = lb_left_value - pow(chosen_x, 2) - 1;
        if (lb_value_under_sqr > 0) {
            double lb_value = sqrt(lb_value_under_sqr);
            printf("%.7lf", lb_value);
        } else {
            printf("-");
        }
        printf(" | ");

        if (chosen_x != 0) {
            double hyperbola_value = 1 / (pow(chosen_x, 2));
            printf("%.7lf", hyperbola_value);
        } else {
            printf("-");
        }
        printf("\n");

        iteration++;
    }
}
