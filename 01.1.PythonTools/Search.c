#include <stdio.h>
#include <math.h>
#define NMAX 10

int input(int *a, int *n);
double mean(int *a, int n);
double sigma(int *a, int n);
int should_display_current_value(int current_value, double mean_value, double sigma_value);

int main()
{
    int n, data[NMAX];
    input(data, &n);

    double mean_value = mean(data, n);
    double sigma_value = sigma(data, n);
    for(int *p = data; p - data < n; p++)
    {
        if (should_display_current_value(*p, mean_value, sigma_value) == 1) {
            printf("%d", *p);
            if ((p - data) < (n-1)) {
                printf(" ");
            }
        }
    }
    printf("\n");
    return 0;
}

int input(int *a, int *n) {
    scanf("%d", n);
    for(int *p = a; p - a < *n; p++)
    {
        scanf("%d", p);
    }
}

double mean(int *a, int n) {
    int current_amount = 0;
    double current_mean = 0.0;
    for(int *p = a; p - a < n; p++)
    {
        current_amount++;
        current_mean += ((*p) - current_mean) / current_amount;
    }
    return current_mean;
};

double sigma(int *a, int n) {
    double mean_value = mean(a, n);
    double current_variance = 0.0;
    for(int *p = a; p - a < n; p++)
    {
        double variance_update = (*p - mean_value);
        current_variance += (variance_update*variance_update / n);
    }
    return sqrt(current_variance);
};

int should_display_current_value(int current_value, double mean_value, double sigma_value) {
    if (current_value % 2 == 1) {
        return 0;
    }
    if (current_value < mean_value) {
        return 0;
    }
    if ((current_value - mean_value) > 3*sigma_value) {
        return 0;
    }
    return 1;
}
