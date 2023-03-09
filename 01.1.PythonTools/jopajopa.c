#include <stdio.h>
#include <stdlib.h>

int input(int **a, int* n);
void output(int* a, int n);
void merge_sort(int* a, int n);
void merge_sort_internal(int* a, int start_index_inclusive, int end_index_exclusive, int n);
void merge_two_sub_arrays(int* a, int start_index_inclusive, int middle_index, int end_index_exclusive, int n);

int main() {
    int* data = NULL;
    int n;
    if (input(&data, &n) == 0) {
        merge_sort(data, n);
        output(data, n);
        free(data);
    } else {
        printf("n/a");
    }
    return 0;
}

int input(int** a, int *n) {
    int result = 0;
    if (scanf("%d", n) != 1) {
        result = 1;
    } else {
        if (*n < 1) {
            result = 1;
        }
        *a = (int *)malloc(*n * sizeof(int));
        for (int *p = *a; ((p - *a < *n) && result == 0); p++) {
            if (scanf("%d", p) != 1) {
                result = 1;
            }
        }
    }
    return result;
}


void output(int* a, int n) {
    for (int* p = a; p - a < n; p++) {
        printf("%d", *p);
        if ((p - a) < (n - 1)) {
            printf(" ");
        }
    }
}

void merge_sort(int* a, int n) { merge_sort_internal(a, 0, n, n); }

void merge_sort_internal(int* a, int start_index_inclusive, int end_index_exclusive, int n) {
    if (start_index_inclusive < (end_index_exclusive - 1)) {
        int middle_index = (end_index_exclusive + start_index_inclusive) / 2;
        merge_sort_internal(a, start_index_inclusive, middle_index, n);
        merge_sort_internal(a, middle_index, end_index_exclusive, n);
        merge_two_sub_arrays(a, start_index_inclusive, middle_index, end_index_exclusive, n);
    }
}

void merge_two_sub_arrays(int* a, int start_index_inclusive, int middle_index, int end_index_exclusive, int n) {
    int output_index = 0;
    int left_index = start_index_inclusive;
    int right_index = middle_index;

    int* output_data = (int *)malloc(n * sizeof(int));
    while (left_index < middle_index && right_index < end_index_exclusive) {
        if (a[left_index] < a[right_index]) {
            output_data[output_index] = a[left_index];
            left_index++;
            output_index++;
        } else {
            output_data[output_index] = a[right_index];
            right_index++;
            output_index++;
        }
    }
    while (left_index < middle_index) {
        output_data[output_index] = a[left_index];
        left_index++;
        output_index++;
    }
    while (right_index < end_index_exclusive) {
        output_data[output_index] = a[right_index];
        right_index++;
        output_index++;
    }

    for (int i = start_index_inclusive; i < end_index_exclusive; i++) {
        a[i] = output_data[i - start_index_inclusive];
    }
    free(output_data);
}
