#include <math.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    double epsilon = 1e-10;

    double begin_x = -M_PI;
    double end_x = M_PI;
    double step_x = (end_x - begin_x) / 41;


    // First: VA function
    {
        double begin_y = 0.092000 * 0.9;
        double end_y = 0.994163 * 1.1;
        double step_y = (end_y - begin_y) / 21;

        int iteration = 0;
        for (double current_y = end_y; current_y > (begin_y + epsilon); current_y -= step_y) {
            for (double current_x = begin_x; current_x <= (end_x + epsilon); current_x += step_x) {
                double chosen_x;
                if (iteration == 41) {
                    chosen_x = end_x;
                } else {
                    chosen_x = current_x;
                }

                double y_from_function = 1 / (1 + pow(chosen_x, 2));

                double next_y = current_y - step_y;
                if (y_from_function >= next_y && y_from_function <= current_y) {
                    printf("*");
                } else {
                    printf(" ");
                }
            }
            printf("\n");

            iteration++;
        }
    }

    // Second: LB function
    {
        double begin_y = 0.0761782 * 0.9;
        double end_y = 0.4996003 * 1.1;
        double step_y = (end_y - begin_y) / 21;

        int iteration = 0;
        for (double current_y = end_y; current_y > (begin_y + epsilon); current_y -= step_y) {
            for (double current_x = begin_x; current_x <= (end_x + epsilon); current_x += step_x) {
                double chosen_x;
                if (iteration == 41) {
                    chosen_x = end_x;
                } else {
                    chosen_x = current_x;
                }

                double lb_left_value = sqrt(1 + 4 * pow(chosen_x, 2));
                double lb_value_under_sqr = lb_left_value - pow(chosen_x, 2) - 1;
                if (lb_value_under_sqr > 0) {
                    double y_from_function =  sqrt(lb_value_under_sqr);
                    double next_y = current_y - step_y;
                    if (y_from_function >= next_y && y_from_function <= current_y) {
                        printf("*");
                    } else {
                        printf(" ");
                    }
                } else {
                    printf(" ");
                }

            }
            printf("\n");

            iteration++;
        }
    }

    // Third: LB function
    {
        double begin_y = 0.101321 * 0.9;
        double end_y = 170.320910 * 1.1;
        double step_y = (end_y - begin_y) / 21;

        int iteration = 0;
        for (double current_y = end_y; current_y > (begin_y + epsilon); current_y -= step_y) {
            for (double current_x = begin_x; current_x <= (end_x + epsilon); current_x += step_x) {
                double chosen_x;
                if (iteration == 41) {
                    chosen_x = end_x;
                } else {
                    chosen_x = current_x;
                }

                double hyperbola_value = 1 / (pow(chosen_x, 2));
                double y_from_function =  hyperbola_value;
                double next_y = current_y - step_y;
                if (y_from_function >= next_y && y_from_function <= current_y) {
                    printf("*");
                } else {
                    printf(" ");
                }
            }
            printf("\n");

            iteration++;
        }
    }
}
