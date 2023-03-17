#include <stdio.h>
#include "bst.h"

int value_comparator(int left_value, int right_value) {
    if (left_value < right_value) {
        return -1;
    } else if (left_value > right_value) {
        return 1;
    }
    return 0;
}

int test_bstree_insert() {
    int test_has_failed = 0;

    int root_value = 10;
    t_btree* root_node = bstree_create_node(root_value);
    if (root_node == NULL || root_node->item != root_value) {
        test_has_failed = 1;
    }

    int left_value = 5;
    bstree_insert(root_node, left_value, value_comparator);
    int right_value = 15;
    bstree_insert(root_node, right_value, value_comparator);

    if (root_node->left == NULL || root_node->left->item != left_value) {
        test_has_failed = 1;
    }
    if (root_node->right == NULL || root_node->right->item != right_value) {
        test_has_failed = 1;
    }

    if (test_has_failed == 0) {
        printf("SUCCESS\n");
    } else {
        printf("FAIL\n");
    }
    return test_has_failed;
}

int main() {
    printf("Launch tree insert test\n");
    test_bstree_insert();
    return 0;
}