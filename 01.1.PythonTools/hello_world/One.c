#include <stdio.h>
#include <stdlib.h>

int input(int*** matrix, int* row_amount, int* col_amount);
void output(int** matrix, int n, int m);

int main() {
    int** matrix;
    int row_amount, col_amount;
    if ()
    return 0;
}



int input(int*** matrix, int* row_amount, int* col_amount) {
    int amount_scanned = scanf("%d%d", row_amount, col_amount);
    if ((amount_scanned != 2) || (*row_amount < 1) || (*col_amount) < 1) {
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
