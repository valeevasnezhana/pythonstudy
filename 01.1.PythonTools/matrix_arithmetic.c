#include <stdio.h>
#include <stdlib.h>

int input_mode(int* mode);
int input(int*** matrix, int* row_amount, int* col_amount);
int errors_handler(int mode, int*** matrix1, int* row_amount1, int* col_amount1, int*** matrix2, int* row_amount2, int* col_amount2);
void output(int **matrix, int n, int m);
void sum(int **matrix_first, int n_first, int m_first, int **matrix_second, int **matrix_result);
void transpose(int **matrix, int n, int m, int **result);
void mul(int **matrix_first, int n_first, int **matrix_second, int n_second, int m_second,
        int **matrix_result);
void operation_handler(int mode, int **matrix_first, int n_first, int m_first, int **matrix_second, int n_second, int m_second);

int main() {
    int mode;
    int error_mode = input_mode(&mode);
    if (error_mode == 1) {
        printf("n/a");
    } else {
        int** matrix1;
        int row_amount1, col_amount1;
        int** matrix2;
        int row_amount2, col_amount2;
        if (errors_handler(mode, &matrix1, &row_amount1, &col_amount1, &matrix2, &row_amount2, &col_amount2) == 1) {
            printf("n/a");
        } else {
            operation_handler(mode, matrix1, row_amount1, col_amount1, matrix2, row_amount2, col_amount2);
        }

    }
    return 0;
}

void operation_handler(int mode, int **matrix_first, int n_first, int m_first, int **matrix_second, int n_second, int m_second) {
    int** result = malloc((n_first) * (m_first) * sizeof(int) + (n_first) * sizeof(int*));
    int* ptr = (int*)((result) + (n_first));
    for (int row_index = 0; row_index < n_first; row_index++) {
        (result)[row_index] = ptr + (m_first) * row_index;
    }
    if (mode == 3) {
        transpose(matrix_first, n_first, m_first, result);
        output(result, m_first, n_first);
    } else if (mode == 1) {
        sum(matrix_first, n_first, m_first, matrix_second, result);
        output(result, n_first, m_first);
        free(matrix_second);
    } else if (mode == 2) {
        mul(matrix_first, n_first, matrix_second, n_second, m_second, result);
        output(result, n_first, m_second);
        free(matrix_second);
    }
    free(result);
    free(matrix_first);
}


int input_mode(int* mode){
    int result = 1;
    if (scanf("%d", mode) == 1) {
        if ((*mode < 4) && (*mode > 0)) {
            result = 0;
        }
    }
    return result;
}

int errors_handler(int mode, int*** matrix1, int* row_amount1, int* col_amount1, int*** matrix2, int* row_amount2, int* col_amount2) {
    int result = 0;
    if (mode == 1 || mode == 2){
        if ((input(matrix1, row_amount1, col_amount1) == 1) || (input(matrix2, row_amount2, col_amount2) == 1)) {
            result = 1;
        } else if ((mode == 1) && ((*row_amount2 != *row_amount1) || (*col_amount1 != *col_amount2))) {
            result = 1;
        } else if ((mode == 2) && (*col_amount1 != *row_amount2)) {
            result = 1;
        }
    } else if (mode == 3) {
        if (input(matrix1, row_amount1, col_amount1) == 1) {
            result = 1;
        }
    }
    return result;
}

int input(int*** matrix, int* row_amount, int* col_amount)  {
    int amount_scanned = scanf("%d%d", row_amount, col_amount);
    if ((amount_scanned != 2) || (*row_amount < 1) || (*col_amount) < 1 ) {
        return 1;
    }
    *matrix = malloc((*row_amount) * (*col_amount) * sizeof(int) + (*row_amount) * sizeof(int*));
    int* ptr = (int*)((*matrix) + (*row_amount));
    for (int row_index = 0; row_index < *row_amount; row_index++) {
        (*matrix)[row_index] = ptr + (*col_amount) * row_index;
    }

    for (int row_index = 0; row_index < *row_amount; row_index++) {
        for (int col_index = 0; col_index < *col_amount; col_index++) {
            int input_value;
            int amount_scanned = scanf("%d", &input_value);
            if (amount_scanned != 1) {
                free(*matrix);
                return 1;
            }
            (*matrix)[row_index][col_index] = input_value;
        }
    }
    return 0;
}


void output(int** matrix, int row_amount, int col_amount) {
    for (int row_index = 0; row_index < row_amount; row_index++) {
        for (int col_index = 0; col_index < col_amount; col_index++) {
            int current_value = matrix[row_index][col_index];
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


void sum(int **matrix_first, int n_first, int m_first, int **matrix_second, int **matrix_result) {
    for (int row = 0; row < n_first; row++){
        for (int col = 0; col < m_first; col++){
            matrix_result[row][col] = matrix_first[row][col] + matrix_second[row][col];
        }
    }
}

void transpose(int **matrix, int n, int m, int **result) {
    for (int row = 0; row < n; row++){
        for (int col = 0; col < m; col++){
            result[col][row] = matrix[row][col];
        }
    }

}

void mul(int **matrix_first, int n_first, int **matrix_second, int n_second, int m_second,
         int **matrix_result) {
    for (int row1 = 0; row1 < n_first; row1++) {
        for (int col2 = 0; col2 < m_second; col2++) {
            matrix_result[row1][col2] = 0;
            for (int row2 = 0; row2 < n_second; row2++) {
                matrix_result[row1][col2] += matrix_first[row1][row2] * matrix_second[row2][col2];
            }
        }
    }
}
