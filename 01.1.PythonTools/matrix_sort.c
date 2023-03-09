#include <stdio.h>
#include <stdlib.h>

#define NMAX_STATIC 100

int input(int*** matrix, int* row_amount, int* col_amount, int* mode, int* memory_was_allocated);

int input_dynamic(int*** matrix, int row_amount, int col_amount, int mode, int* memory_was_allocated);

void allocate_dynamic_matrix(int*** matrix, int row_amount, int col_amount, int mode, int* memory_was_allocated);

int output(int** matrix, int row_amount, int col_amount, int mode);

int get_element(int** matrix, int row_index, int col_index, int mode);

int free_all(int** matrix, int row_amount, int col_amount, int mode);

int* create_row_sum_array(int** matrix, int row_amount, int col_amount);

void swap_numbers(int* array, int left_index, int right_index);

void swap_rows(int** matrix, int left_row_index, int right_row_index, int mode);

void sort_matrix(int** matrix, int row_amount, int col_amount, int mode);

int main() {
    int** matrix;
    int row_amount, col_amount, mode;
    int memory_was_allocated = 0;

    int error_amount = input(&matrix, &row_amount, &col_amount, &mode, &memory_was_allocated);
    if (error_amount > 0) {
        printf("n/a");
    } else {
        sort_matrix(matrix, row_amount, col_amount, mode);
        output(matrix, row_amount, col_amount, mode);
        if (memory_was_allocated == 1) {
            free_all(matrix, row_amount, col_amount, mode);
        }
    }

    return 0;
}

int input(int*** matrix, int* row_amount, int* col_amount, int* mode, int* memory_was_allocated) {
    int amount_scanned = scanf("%d%d%d", mode, row_amount, col_amount);
    int return_code;
    if (amount_scanned != 3 || *mode < 1 || *mode > 4) {
        return_code = 1;
    } else {
        return_code = input_dynamic(matrix, *row_amount, *col_amount, *mode, memory_was_allocated);
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
    if (mode == 1) {
        *matrix = (int**) malloc((row_amount) * (col_amount) * sizeof(int) + (row_amount) * sizeof(int*));
        int* ptr = (int*) ((*matrix) + (row_amount));
        for (int row_index = 0; row_index < row_amount; row_index++) {
            (*matrix)[row_index] = ptr + (col_amount) * row_index;
        }
        *memory_was_allocated = 1;
    } else if (mode == 2) {
        *matrix = (int**) malloc((row_amount) * sizeof(int*));
        for (int row_index = 0; row_index < row_amount; row_index++) {
            (*matrix)[row_index] = malloc((col_amount) * sizeof(int));
        }
        *memory_was_allocated = 1;
    } else if (mode == 3) {
        *matrix = (int**) malloc((row_amount) * sizeof(int*));
        int* values_array = malloc((row_amount) * (col_amount) * sizeof(int));
        for (int row_index = 0; row_index < row_amount; row_index++) {
            (*matrix)[row_index] = values_array + (col_amount) * row_index;
        }
        *memory_was_allocated = 1;
    }
}

int* create_row_sum_array(int** matrix, int row_amount, int col_amount) {
    int* row_sum_array = (int*) malloc(row_amount * sizeof(int));
    for (int row_index = 0; row_index < row_amount; row_index++) {
        int current_row_sum = 0;
        for (int col_index = 0; col_index < col_amount; col_index++) {
            current_row_sum += matrix[row_index][col_index];
        }
        row_sum_array[row_index] = current_row_sum;
    }
    return row_sum_array;
}

void swap_numbers(int* array, int left_index, int right_index) {
    int tmp = array[left_index];
    array[left_index] = array[right_index];
    array[right_index] = tmp;
}

void swap_rows(int** matrix, int left_row_index, int right_row_index, int mode) {
    if (mode == 1 || mode == 2) {
        int* tmp = matrix[left_row_index];
        matrix[left_row_index] = matrix[right_row_index];
        matrix[right_row_index] = tmp;
    } else if (mode == 3) {
        // this mode not supported
    }
}

void sort_matrix(int** matrix, int row_amount, int col_amount, int mode) {
    int* row_sum_array = create_row_sum_array(matrix, row_amount, col_amount);
    for (int iteration = 0; iteration < row_amount; iteration++) {
        for (int current_index = 1; current_index < row_amount; current_index++) {
            int prev_index = current_index - 1;
            if (row_sum_array[prev_index] > row_sum_array[current_index]) {
                swap_numbers(row_sum_array, prev_index, current_index);
                swap_rows(matrix, prev_index, current_index, mode);
            }
        }
    }
    free(row_sum_array);
}

int output(int** matrix, int row_amount, int col_amount, int mode) {
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            int current_value = get_element(matrix, row_index, col_index, mode);
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

int get_element(int** matrix, int row_index, int col_index, int mode) {
    int output_value;
    output_value = matrix[row_index][col_index];
    return output_value;
}

int free_all(int** matrix, int row_amount, int col_amount, int mode) {
    if (mode == 1) {
        free(matrix);
    } else if (mode == 2) {
        for (int row_index = 0; row_index < row_amount; row_index++) {
            free(matrix[row_index]);
        }
        free(matrix);
    } else if (mode == 3) {
        free(matrix[0]);
        free(matrix);
    }
}