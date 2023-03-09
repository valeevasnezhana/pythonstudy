#include <stdio.h>
#include <stdlib.h>

#define NMAX_STATIC 100

int input(int*** matrix, int static_matrix[][NMAX_STATIC], int* row_amount, int* col_amount, int* mode, int* memory_was_allocated);
int input_static(int static_matrix[][NMAX_STATIC], int row_amount, int col_amount);
int input_dynamic(int*** matrix, int row_amount, int col_amount, int mode, int* memory_was_allocated);
void allocate_dynamic_matrix(int*** matrix, int row_amount, int col_amount, int mode, int* memory_was_allocated);

int output(int** matrix, int static_matrix[][NMAX_STATIC], int row_amount, int col_amount, int mode);
int get_element(int** matrix, int static_matrix[][NMAX_STATIC], int row_index, int col_index, int mode);
int free_all(int** matrix, int static_matrix[][NMAX_STATIC], int row_amount, int col_amount, int mode);

int main() {
    int static_matrix[NMAX_STATIC][NMAX_STATIC];
    int** matrix;
    int row_amount, col_amount, mode;
    int memory_was_allocated = 0;

    int error_amount = input(&matrix, static_matrix, &row_amount, &col_amount, &mode, &memory_was_allocated);
    if (error_amount > 0) {
        printf("n/a");
    } else {
        output(matrix, static_matrix, row_amount, col_amount, mode);
        if (memory_was_allocated == 1) {
            free_all(matrix, static_matrix, row_amount, col_amount, mode);
        }
    }

    return 0;
}

int input(int*** matrix, int static_matrix[][NMAX_STATIC], int* row_amount, int* col_amount, int* mode, int* memory_was_allocated) {
    int amount_scanned = scanf("%d%d%d", mode, row_amount, col_amount);
    int return_code;
    if (amount_scanned != 3 || *mode < 1 || *mode > 4) {
        return_code = 1;
    } else if (*mode == 1) {
        return_code = input_static(static_matrix, *row_amount, *col_amount);
    } else {
        return_code = input_dynamic(matrix, *row_amount, *col_amount, *mode, memory_was_allocated);
    }
    return return_code;
}

int input_static(int static_matrix[][NMAX_STATIC], int row_amount, int col_amount) {
    int return_code = 0;
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            int amount_scanned = scanf("%d", &static_matrix[row_index][col_index]);
            if (amount_scanned != 1) {
                return_code = 1;
                break;
            }
        }
    }
    return return_code;
}

int input_dynamic(int*** matrix, int row_amount, int col_amount, int mode, int* memory_was_allocated) {
    allocate_dynamic_matrix(matrix, row_amount, col_amount, mode, memory_was_allocated);
    int return_code = 0;
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            int input_value;
            int amount_scanned = scanf("%d", &input_value);
            if (amount_scanned != 1) {
                return_code = 1;
                break;
            }
            (*matrix)[row_index][col_index] = input_value;
        }
    }
    return return_code;
}

void allocate_dynamic_matrix(int*** matrix, int row_amount, int col_amount, int mode, int* memory_was_allocated) {
    if (mode == 2) {
        *matrix = malloc((row_amount) * (col_amount) * sizeof(int) + (row_amount) * sizeof(int*));
        int* ptr = (int*) ((*matrix) + (row_amount));
        for (int row_index = 0; row_index < row_amount; row_index++) {
            (*matrix)[row_index] = ptr + (col_amount) * row_index;
        }
        *memory_was_allocated = 1;
    } else if (mode == 3) {
        *matrix = malloc((row_amount) * sizeof(int*));
        for (int row_index = 0; row_index < row_amount; row_index++) {
            (*matrix)[row_index] = malloc((col_amount) * sizeof(int));
        }
        *memory_was_allocated = 1;
    } else if (mode == 4) {
        *matrix = malloc((row_amount) * sizeof(int*));
        int* values_array = malloc((row_amount) * (col_amount) * sizeof(int));
        for (int row_index = 0; row_index < row_amount; row_index++) {
            (*matrix)[row_index] = values_array + (col_amount) * row_index;
        }
        *memory_was_allocated = 1;
    }
}

int output(int** matrix, int static_matrix[][NMAX_STATIC], int row_amount, int col_amount, int mode) {
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            int current_value = get_element(matrix, static_matrix, row_index, col_index, mode);
            printf("%d", current_value);
            if (col_index < (col_amount - 1)) {
                printf(" ");
            }
        }
        if (row_index < (row_amount - 1)) {
            printf("\n");
        }
    }
}

int get_element(int** matrix, int static_matrix[][NMAX_STATIC], int row_index, int col_index, int mode) {
    int output_value;
    if (mode == 1) {
        output_value = static_matrix[row_index][col_index];
    } else {
        output_value = matrix[row_index][col_index];
    }
    return output_value;
}

int free_all(int** matrix, int static_matrix[][NMAX_STATIC], int row_amount, int col_amount, int mode) {
    if (mode == 2) {
        free(matrix);
    } else if (mode == 3) {
        for (int row_index = 0; row_index < row_amount; row_index++) {
            free(matrix[row_index]);
        }
        free(matrix);
    } else if (mode == 4) {
        free(matrix[0]);
        free(matrix);
    }
}