#include <stdio.h>
#include "bst.h"

void applyf(int input_value){
    printf("Tree value: %d\n", input_value);
}

int value_comparator(int left_value, int right_value) {
    if (left_value < right_value) {
        return -1;
    } else if (left_value > right_value) {
        return 1;
    }
    return 0;
}

int test_bstree_create_node() {
    int test_has_failed = 0;

    int root_value = 10;
    t_btree* root_node = bstree_create_node(root_value);
    if (root_node == NULL || root_node->item != root_value) {
        test_has_failed = 1;
    }
    for (int current_value = 0; current_value < 5; current_value++) {
        bstree_insert(root_node, current_value, value_comparator);
    }
    for (int current_value = 10; current_value >= 5; current_value--) {
        bstree_insert(root_node, current_value, value_comparator);
    }

    printf("\n+++ Test apply infix\n");
    bstree_apply_infix(root_node, applyf);

    printf("\n+++ Test apply prefix\n");
    bstree_apply_prefix(root_node, applyf);

    printf("\n+++ Test apply infix\n");
    bstree_apply_postfix(root_node, applyf);

    if (test_has_failed == 0) {
        printf("SUCCESS\n");
    } else {
        printf("FAIL\n");
    }
    return test_has_failed;
}

int main() {
    test_bstree_create_node();
    return 0;
}