#include <stdio.h>
#include <stdlib.h>

/*
    1 6 7
    2 5 8
    3 4 9
*/
void sort_vertical(int **matrix, int n, int m, int **result_matrix);

/*
    1 2 3
    6 5 4
    7 8 9
*/
void sort_horizontal(int **matrix, int n, int m, int **result_matrix);

int input(int*** matrix, int* row_amount, int* col_amount, int* memory_was_allocated);
void output(int** matrix, int row_amount, int col_amount, int include_newline);
void allocate_dynamic_matrix(int*** matrix, int row_amount, int col_amount);
void create_temp_arr(int **matrix, int n, int m, int** temp_arr);
void bubble_sort(int* arr, int arr_len);

int main() {
    int** matrix, **result;
    int row_amount, col_amount;
    int memory_was_allocated = 0;
    int return_code = input(&matrix, &row_amount, &col_amount, &memory_was_allocated);
    if (return_code == 0) {
        allocate_dynamic_matrix(&result, row_amount, col_amount);
        sort_vertical(matrix, row_amount, col_amount, result);
        output(result, row_amount, col_amount, 1);
        sort_horizontal(matrix, row_amount, col_amount, result);
        output(result, row_amount, col_amount, 0);
    } else {
        printf("n/a");
    }
    if (memory_was_allocated) {
        free(matrix);
    }
}

void sort_vertical(int **matrix, int n, int m, int **result_matrix) {
    int* temp_arr;
    create_temp_arr(matrix, n, m, &temp_arr);
    bubble_sort(temp_arr, n * m);
    for (int row_index = 0; row_index < n; row_index++) {
        for (int col_index = 0; col_index < m; col_index++) {
            int input_index;
            if (col_index % 2 == 0) {
                input_index = col_index * n + row_index;
            } else {
                input_index = col_index * n + (n - 1) - row_index;
            }
            int input_value = temp_arr[input_index];
            result_matrix[row_index][col_index] = input_value;
        }
    }
    free(temp_arr);
}

void sort_horizontal(int **matrix, int n, int m, int **result_matrix) {
    int* temp_arr;
    create_temp_arr(matrix, n, m, &temp_arr);
    bubble_sort(temp_arr, n * m);
    for (int row_index = 0; row_index < n; row_index++) {
        for (int col_index = 0; col_index < m; col_index++) {
            int input_index;
            if (row_index % 2 == 0) {
                input_index = row_index * m + col_index;
            } else {
                input_index = row_index * m + (m - 1) - col_index;
            }
            result_matrix[row_index][col_index] = temp_arr[input_index];
        }
    }
    free(temp_arr);
}

int input(int*** matrix, int* row_amount, int* col_amount, int* memory_was_allocated) {
    int amount_scanned = scanf("%d%d", row_amount, col_amount);
    if ((amount_scanned != 2) || (*row_amount < 1) || (*col_amount) < 1) {
        return 1;
    }
    allocate_dynamic_matrix(matrix, *row_amount, *col_amount);
    *memory_was_allocated = 1;

    for (int row_index = 0; row_index < *row_amount; row_index++) {
        for (int col_index = 0; col_index < *col_amount; col_index++) {
            int input_value;
            int amount_scanned = scanf("%d", &input_value);
            if (amount_scanned != 1) {
                return 1;
            }
            (*matrix)[row_index][col_index] = input_value;
        }
    }
    return 0;
}

void output(int** matrix, int row_amount, int col_amount, int include_newline) {
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            printf("%d", matrix[row_index][col_index]);
            if (col_index < col_amount - 1) {
                printf(" ");
            }
        }
        if (row_index < row_amount - 1) {
            printf("\n");
        }
    }
    if (include_newline == 1) {
        printf("\n\n");
    }
}

void allocate_dynamic_matrix(int*** matrix, int row_amount, int col_amount) {
    *matrix = (int**) malloc((row_amount) * (col_amount) * sizeof(int) + (row_amount) * sizeof(int*));
    int* ptr = (int*) ((*matrix) + (row_amount));
    for (int row_index = 0; row_index < row_amount; row_index++) {
        (*matrix)[row_index] = ptr + (col_amount) * row_index;
    }
}


void create_temp_arr(int **matrix, int n, int m, int** temp_arr) {
    *temp_arr = (int*) malloc(n * m * sizeof(int));
    for (int row_index = 0; row_index < n; row_index++) {
        for (int col_index = 0; col_index < m; col_index++) {
            (*temp_arr)[col_index + row_index * m] = matrix[row_index][col_index];
        }
    }
}

void bubble_sort(int* arr, int arr_len) {
    for (int iteration = 0; iteration < arr_len; iteration++){
        for (int current_index = 1; current_index < arr_len; current_index++){
            int prev_index = current_index - 1;
            if (arr[current_index] < arr[prev_index]) {
                int tmp = arr[current_index];
                arr[current_index] = arr[prev_index];
                arr[prev_index] = tmp;
            }
        }
    }
}