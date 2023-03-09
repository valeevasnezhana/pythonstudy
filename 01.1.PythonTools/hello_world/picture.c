#include <stdio.h>
#define N 15
#define M 13

void transform(int (*buf)[M], int **matr, int n, int m);
void make_picture(int **picture, int n, int m);
void reset_picture(int **picture, int n, int m);

void add_frame(int **picture, int n, int m, int* frame_w, int* frame_h, int length_frame_w, int length_frame_h);
void add_tree(int **picture, int n, int m, int* tree_trunk, int* tree_foliage, int length_tree_trunk, int length_tree_foliage);
void output_picture(int **picture, int n, int m);

void main()
{
    int picture_data[N][M];
    int *picture[N];
    transform(picture_data, picture, N, M);

    make_picture(picture, N, M);
    output_picture(picture, N, M);
}

void make_picture(int **picture, int n, int m)
{
    int frame_w[] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
    int frame_h[] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
    int tree_trunk[] = { 7, 7, 7, 7 };
    int tree_foliage[] = { 3, 3, 3, 3 };
    int sun_data[6][5] = { { 0, 6, 6, 6, 6 },
                           { 0, 0, 6, 6, 6 },
                           { 0, 0, 6, 6, 6 },
                           { 0, 6, 0, 0, 6 },
                           { 0, 0, 0, 0, 0 },
                           { 0, 0, 0, 0, 0 } };
    reset_picture(picture, n, m);
    int length_frame_w = sizeof(frame_w) / sizeof(frame_w[0]);
    int length_frame_h = sizeof(frame_h) / sizeof(frame_h[0]);
    add_frame(picture, n, m, frame_w, frame_h, length_frame_w, length_frame_h);

    int length_tree_trunk = sizeof(tree_trunk) / sizeof(tree_trunk[0]);
    int length_tree_foliage = sizeof(tree_foliage) / sizeof(tree_foliage[0]);
    add_tree(picture, n, m, tree_trunk, tree_foliage, length_tree_trunk, length_tree_foliage);

    int height_sun_data = sizeof(sun_data) / sizeof(sun_data[0]);
    int length_sun_data = sizeof(sun_data[0]) / sizeof(sun_data[0][0]);
    for (int i = 0; i < height_sun_data; i++) {
        for (int j = 0; j < length_sun_data; j++) {
            picture[1+i][7+j] = sun_data[i][j];
        }
    }
}

void reset_picture(int **picture, int n, int m)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            picture[i][j] = 0;
        }
    }
}

void add_frame(int **picture, int n, int m, int* frame_w, int* frame_h, int length_frame_w, int length_frame_h) {
    for (int i = 0; i < length_frame_w; i++)
    {
        picture[0][i] = frame_w[i];
        picture[n/2][i] = frame_w[i];
        picture[n-1][i] = frame_w[i];
    }


    for (int i = 0; i < length_frame_h; i++)
    {
        picture[i][0] = frame_h[i];
        picture[i][m/2] = frame_h[i];
        picture[i][m-1] = frame_h[i];
    }
}

void add_tree(int **picture, int n, int m, int* tree_trunk, int* tree_foliage, int length_tree_trunk, int length_tree_foliage) {
    for (int trunk_index = 0; trunk_index < length_tree_trunk; trunk_index++) {
        picture[10][2+trunk_index] = tree_trunk[trunk_index];
    }
    int input_trunk_index = 0;
    for (int trunk_index = 0; trunk_index < length_tree_trunk+1; trunk_index++) {
        int row = 6 + trunk_index;
        if (row != n/2) {
            picture[row][3] = tree_trunk[input_trunk_index];
            picture[row][4] = tree_trunk[input_trunk_index];
            input_trunk_index++;
        }
    }

    for (int i = 0; i < length_tree_foliage; i++) {
        picture[3][i+2] = tree_foliage[i];
        picture[4][i+2] = tree_foliage[i];
        picture[i+2][3] = tree_foliage[i];
        picture[i+2][4] = tree_foliage[i];
    }
}

void transform(int (*buf)[M], int **matr, int n, int m)
{
    for(int i = 0; i < n; i++)
    {
        matr[i] = buf[i];
    }
}

void output_picture(int **picture, int n, int m) {
    for (int row_index = 0; row_index < n; row_index++) {
        for (int col_index = 0; col_index < m; col_index++) {
            printf("%d", picture[row_index][col_index]);
            if (col_index < (m - 1)) {
                printf(" ");
            }
        }
        if (row_index < (n - 1)) {
            printf("\n");
        }
    }
}
