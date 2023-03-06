#include <stdio.h>
#define NMAX 10

int input(int *a, int *n);
void output(int *a, int n);
int max(int *a, int n);
int min(int *a, int n);
double mean(int *a, int n);
double variance(int *a, int n);

void output_result(int max_v,
                   int min_v,
                   double mean_v,
                   double variance_v);

int main()
{
    int n, data[NMAX];
    input(data, &n);
    output(data, n);
    if (n < 1) {
        return 0;
    }
    output_result(max(data, n),
                  min(data, n),
                  mean(data, n),
                  variance(data, n));

    return 0;
}

int input(int *a, int *n) {
    scanf("%d", n);
    for(int *p = a; p - a < *n; p++)
    {
        scanf("%d", p);
    }
}

void output(int *a, int n)
{
    for(int *p = a; p - a < n; p++)
    {
        printf("%d", *p);
        if ((p - a) < (n-1)) {
            printf(" ");
        }
    }
    printf("\n");
}

int max(int *a, int n) {
    int current_max = *a;
    for(int *p = a; p - a < n; p++)
    {
        if (*p > current_max) {
            current_max = *p;
        }
    }
    return current_max;
};

int min(int *a, int n) {
    int current_min = *a;
    for(int *p = a; p - a < n; p++)
    {
        if (*p < current_min) {
            current_min = *p;
        }
    }
    return current_min;
};

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

double variance(int *a, int n) {
    double mean_value = mean(a, n);
    double current_variance = 0.0;
    for(int *p = a; p - a < n; p++)
    {
        double variance_update = (*p - mean_value);
        current_variance += variance_update*variance_update / n;
    }
    return current_variance;
};

void output_result(int max_v,
                   int min_v,
                   double mean_v,
                   double variance_v) {
    printf("%d %d %.6lf %.6lf\n", max_v, min_v, mean_v, variance_v);
};
