#include <stdio.h>
#include <stdlib.h>

int sle(double** matrix, int n, int m, double* roots);
int input(double*** matrix, int* row_amount, int* col_amount, int* memory_was_allocated);
void output(double** matrix, int row_amount, int col_amount);
void output_roots(double* roots, int n);
void allocate_dynamic_matrix(double*** matrix, int row_amount, int col_amount);
int make_matrix_diagonal(double** matrix, int n, int m);

int main() {
    double** matrix;
    double* roots;
    int row_amount, col_amount;
    int memory_was_allocated = 0;
    int input_return_code = input(&matrix, &row_amount, &col_amount, &memory_was_allocated);
    if (input_return_code == 0) {
        roots = (double*) malloc(row_amount * sizeof(double));
        int sle_return_code = sle(matrix, row_amount, col_amount, roots);
        if (sle_return_code == 0) {
            output_roots(roots, row_amount);
        } else {
            printf("n/a");
        }
    } else {
        printf("n/a");
    }
    if (memory_was_allocated) {
        free(matrix);
        free(roots);
    }
    return 0;
}

int sle(double** matrix, int n, int m, double* roots) {
    int return_code = make_matrix_diagonal(matrix, n, m);
    if (return_code == 0) {
        roots[n - 1] = matrix[n - 1][m - 1] / matrix[n - 1][n - 1];
        for (int iteration = n - 2; iteration >= 0; iteration--) {
            roots[iteration] = matrix[iteration][m - 1];
            for (int col_index = iteration + 1; col_index < n; col_index++) {
                roots[iteration] -= matrix[iteration][col_index] * roots[col_index];
            }
            roots[iteration] /= matrix[iteration][iteration];
        }
    }
    return return_code;
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

void output_roots(double* roots, int n) {
    for (int index = 0; index < n; index++) {
        printf("%lf", roots[index]);
        if (index < (n - 1)) {
            printf(" ");
        }
    }
}

void allocate_dynamic_matrix(double*** matrix, int row_amount, int col_amount) {
    *matrix = (double**) malloc((row_amount) * (col_amount) * sizeof(double) + (row_amount) * sizeof(double*));
    double* ptr = (double*) ((*matrix) + (row_amount));
    for (int row_index = 0; row_index < row_amount; row_index++) {
        (*matrix)[row_index] = ptr + (col_amount) * row_index;
    }
}

int make_matrix_diagonal(double** matrix, int n, int m) {
    int return_code = 0;
    for (int iteration = 0; iteration < n; iteration++) {
        for (int row_index = iteration + 1; row_index < n; row_index++) {
            double diagonal_value = matrix[iteration][iteration];
            if (diagonal_value == 0.0) {
                return_code = 1;
                break;
            }
            double frac = matrix[row_index][iteration] / diagonal_value;
            for (int col_index = 0; col_index < m; col_index++) {
                matrix[row_index][col_index] = matrix[row_index][col_index] - frac * matrix[iteration][col_index];
            }
        }
    }
    return return_code;
}