#include <stdio.h>
#include "bst.h"

int test_bstree_create_node() {
    int test_has_failed = 0;

    int input_item = 10;
    t_btree* sample_node = bstree_create_node(input_item);
    if (sample_node == NULL || sample_node->item != input_item) {
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
    test_bstree_create_node();
    return 0;
}