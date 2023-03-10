#include <stdio.h>
#include <stdlib.h>

void invert(double **matrix, int n, int m);
int input(double*** matrix, int* row_amount, int* col_amount, int* memory_was_allocated);
void output(double** matrix, int row_amount, int col_amount);
void allocate_dynamic_matrix(double*** matrix, int row_amount, int col_amount);
double det(double **matrix, int n);
void create_minor_matrix(double **matrix, int row_index_remove, int col_index_remove, int matrix_size, double **result);


int main() {
    double** matrix;
    int row_amount, col_amount;
    int memory_was_allocated = 0;
    int return_code = input(&matrix, &row_amount, &col_amount, &memory_was_allocated);
    if (return_code == 0) {
        invert(matrix, row_amount, col_amount);
        output(matrix, row_amount, col_amount);
    } else {
        printf("n/a");
    }
    if (memory_was_allocated) {
        free(matrix);
    }
    return 0;
}

void invert(double **matrix, int n, int m) {
    double **minor_matrix;
    double **transposed_cofactor_matrix;
    allocate_dynamic_matrix(&minor_matrix, n - 1, n - 1);
    allocate_dynamic_matrix(&transposed_cofactor_matrix, n, n);
    double determinant_value = det(matrix, n);
    for (int row_index = 0; row_index < n; row_index++) {
        for (int col_index = 0; col_index < m; col_index++) {
            create_minor_matrix(matrix, row_index, col_index, n, minor_matrix);
            double minor_value = det(minor_matrix, n - 1);
            if ((row_index + col_index) % 2 == 1) {
                minor_value *= -1;
            }
            transposed_cofactor_matrix[col_index][row_index] = minor_value / determinant_value;
        }
    }
    free(minor_matrix);

    for (int row_index = 0; row_index < n; row_index++) {
        for (int col_index = 0; col_index < m; col_index++) {
            matrix[row_index][col_index] = transposed_cofactor_matrix[row_index][col_index];
        }
    }
    free(transposed_cofactor_matrix);
}

int input(double*** matrix, int* row_amount, int* col_amount, int* memory_was_allocated) {
    int amount_scanned = scanf("%d%d", row_amount, col_amount);
    if ((amount_scanned != 2) || (*row_amount < 1) || (*col_amount) < 1) {
        return 1;
    }
    allocate_dynamic_matrix(matrix, *row_amount, *col_amount);
    *memory_was_allocated = 1;

    for (int row_index = 0; row_index < *row_amount; row_index++) {
        for (int col_index = 0; col_index < *col_amount; col_index++) {
            double input_value;
            int amount_scanned = scanf("%lf", &input_value);
            if (amount_scanned != 1) {
                return 1;
            }
            (*matrix)[row_index][col_index] = input_value;
        }
    }
    return 0;
}

void allocate_dynamic_matrix(double*** matrix, int row_amount, int col_amount) {
    *matrix = (double**) malloc((row_amount) * (col_amount) * sizeof(double) + (row_amount) * sizeof(double*));
    double* ptr = (double*) ((*matrix) + (row_amount));
    for (int row_index = 0; row_index < row_amount; row_index++) {
        (*matrix)[row_index] = ptr + (col_amount) * row_index;
    }
}

void output(double** matrix, int row_amount, int col_amount) {
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            printf("%.6lf", matrix[row_index][col_index]);
            if (col_index < col_amount - 1) {
                printf(" ");
            }
        }
        if (row_index < row_amount - 1) {
            printf("\n");
        }
    }
}

double det(double **matrix, int n) {
    double **minor_matrix;
    int minor_matrix_size = n - 1;
    allocate_dynamic_matrix(&minor_matrix, minor_matrix_size, minor_matrix_size);

    double det_value = 0;
    if (n == 1) {
        det_value = matrix[0][0];
    } else if (n == 2){
        det_value = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
    } else {
        int sign = 1;
        for (int col_index = 0; col_index < n; col_index++) {
            create_minor_matrix(matrix, 0, col_index, n, minor_matrix);
            double minor_det_value = det(minor_matrix, n - 1);
            det_value = det_value + sign * matrix[0][col_index] * minor_det_value;
            sign = - sign;
        }
    }
    free(minor_matrix);
    return det_value;
}

void create_minor_matrix(double **matrix, int row_index_remove, int col_index_remove, int matrix_size, double **result) {
    for (int row_index = 0; row_index < row_index_remove; row_index++) {
        for (int col_index = 0; col_index < col_index_remove; col_index++) {
            result[row_index][col_index] = matrix[row_index][col_index];
        }
        for (int col_index = col_index_remove + 1; col_index < matrix_size; col_index++) {
            result[row_index][col_index - 1] = matrix[row_index][col_index];
        }
    }
    for (int row_index = row_index_remove + 1; row_index < matrix_size; row_index++) {
        for (int col_index = 0; col_index < col_index_remove; col_index++) {
            result[row_index - 1][col_index] = matrix[row_index][col_index];
        }
        for (int col_index = col_index_remove + 1; col_index < matrix_size; col_index++) {
            double current_value = matrix[row_index][col_index];
            result[row_index - 1][col_index - 1] = current_value;
        }
    }
}