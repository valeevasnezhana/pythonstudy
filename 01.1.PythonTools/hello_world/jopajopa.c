#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define ROWS 25
#define COLS 80

void output(char matrix[][COLS]);
void copy_matrix(char matrix[][COLS], char buffer[][COLS]);
void fill_start_matrix(char matrix[][COLS], char dead_in_file, char alive, char dead);
void calculate_new_generation (char matrix[][COLS], char buffer[][COLS], char alive, char dead);
int get_neighbours_amount(char matrix[][COLS], int i, int j, char alive);


int main() {
    char start_matrix[ROWS][COLS];
    char next_matrix[ROWS][COLS];
    const char dead_in_file = '-';
    const char dead = ' ';
    const char alive = 'X';
    fill_start_matrix(start_matrix, dead_in_file, alive, dead);
    output(start_matrix);
    copy_matrix(start_matrix, next_matrix);
    while (1 == 1) {
        usleep(200000);
        calculate_new_generation(start_matrix, next_matrix, alive, dead);
        output(next_matrix);
    }
    return 0;
}


void fill_start_matrix(char matrix[][COLS], char dead_in_file, char alive, char dead) {
    char symb;
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            matrix[i][j] = dead;
        }
    }
    int end_cycle = 0;
    for (int i = 0; i < ROWS && !end_cycle; i++) {
        for (int j = 0; j < COLS && !end_cycle; j++) {
            symb = getchar();
            if ((symb != dead_in_file) && (symb != alive) && (symb != '\n')) {
                end_cycle = 1;
            }
            if (symb == alive) {
                matrix[i][j] = symb;

            }
        }
    }
}

void calculate_new_generation(char matrix[][COLS], char buffer[][COLS], char alive, char dead) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            char value = matrix[i][j];

            int nb_count = get_neighbours_amount(matrix, i, j, alive);

            if ((value == alive) && (nb_count < 2 || nb_count > 3)) {
                buffer[i][j] = dead;
                continue;
            }
            if ((value == dead) && nb_count == 3) {
                buffer[i][j] = alive;
            }
        }
    }
    copy_matrix(buffer, matrix);
}

void copy_matrix(char matrix[][COLS], char buffer[][COLS]) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            buffer[i][j] = matrix[i][j];
        }
    }
}

int get_neighbours_amount(char matrix[][COLS], int i, int j, char alive){
    int nb_count = 0;
    for (int nb_x = -1; nb_x <= 1; nb_x++) {
        for (int nb_y = -1; nb_y <= 1; nb_y++) {
            if (!nb_x && !nb_y) {
                continue;
            }
            int real_nb_x = i + nb_x;
            int real_nb_y = j + nb_y;

            if (matrix[real_nb_x % ROWS][real_nb_y % COLS] == alive) {
                nb_count++;
            }
        }
    }
    return nb_count;
}

void output(char matrix[][COLS]) {
    for (int row_index = 0; row_index < ROWS; row_index++) {
        for (int col_index = 0; col_index < COLS; col_index++) {
            int current_value = matrix[row_index][col_index];
            printf("%c", current_value);
        }
        printf("\n");
    }
}


