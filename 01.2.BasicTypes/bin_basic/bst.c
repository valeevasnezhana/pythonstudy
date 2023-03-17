#include <stdlib.h>
#include <stdio.h>
#include "bst.h"


t_btree* bstree_create_node(int item) {
    t_btree* node_p = (t_btree*)malloc(sizeof(t_btree));
    node_p->item = item;
    node_p->left = NULL;
    node_p->right = NULL;
    node_p->parent = NULL;
    return node_p;
}

void bstree_insert(t_btree *root, int item, int (*cmpf) (int, int)) {
    t_btree* new_root = root;
    t_btree* current_node = root;
    while (new_root != NULL){
        if (cmpf(item, new_root->item) < 0){
            current_node = new_root;
            new_root = new_root->left;
        }
        else if (cmpf(item, new_root->item) > 0){
            current_node = new_root;
            new_root = new_root->right;
        }
        else return;
    }
    if (cmpf(item, current_node->item) > 0){
        current_node->right = bstree_create_node(item);
        current_node->right->parent = current_node;
    }
    else if (cmpf(item, current_node->item) < 0){
        current_node->left = bstree_create_node(item);
        current_node->left->parent = current_node;
    }
}

void bstree_apply_infix(t_btree *root, void (*applyf) (int)) {
    t_btree* prev = NULL;
    t_btree* current_node = root;
    while (current_node != NULL){
        if (prev == current_node->parent){
            if(current_node->left != NULL) {
                prev = current_node;
                current_node = current_node->left;
                continue;
            }
        }

        if (prev == current_node->left || prev == current_node->parent){
            applyf(current_node->item);
            if(current_node->right != NULL) {
                prev = current_node;
                current_node = current_node->right;
                continue;
            }
        }

        prev = current_node;
        current_node = current_node->parent;
    }
}

void bstree_apply_prefix(t_btree *root, void (*applyf) (int)) {
    t_btree* prev = NULL;
    t_btree* current_node = root;
    while (current_node != NULL){
        if (prev == current_node->parent){
            applyf(current_node->item);
            if(current_node->left != NULL) {
                prev = current_node;
                current_node = current_node->left;
                continue;
            }
        }

        if (prev == current_node->left || prev == current_node->parent){
            if(current_node->right != NULL) {
                prev = current_node;
                current_node = current_node->right;
                continue;
            }
        }

        prev = current_node;
        current_node = current_node->parent;
    }
}

void bstree_apply_postfix(t_btree *root, void (*applyf) (int)) {
    t_btree* prev = NULL;
    t_btree* current_node = root;
    while (current_node != NULL){
        if (prev == current_node->parent){
            if(current_node->left != NULL) {
                prev = current_node;
                current_node = current_node->left;
                continue;
            }
        }

        if (prev == current_node->left || prev == current_node->parent){
            if(current_node->right != NULL) {
                prev = current_node;
                current_node = current_node->right;
                continue;
            }
        }

        applyf(current_node->item);

        prev = current_node;
        current_node = current_node->parent;
    }
}