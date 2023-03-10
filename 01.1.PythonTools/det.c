#include <stdio.h>
#include <stdlib.h>

double det(double **matrix, int n);
int input(double*** matrix, int* row_amount, int* col_amount, int* memory_was_allocated);
void output(double det);
void allocate_dynamic_matrix(double*** matrix, int row_amount, int col_amount);
void create_minor_matrix(double **matrix, int row_index_remove, int col_index_remove, int matrix_size, double **result);


int main()
{
    double** matrix;
    int row_amount, col_amount;
    int memory_was_allocated = 0;
    int return_code = input(&matrix, &row_amount, &col_amount, &memory_was_allocated);
    if (return_code == 0) {
        double det_value = det(matrix, row_amount);
        output(det_value);
    } else {
        printf("n/a");
    }
    if (memory_was_allocated) {
        free(matrix);
    }
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

void output(double det_value) {
    printf("%.6f", det_value);
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