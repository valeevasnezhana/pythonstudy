#include <stdlib.h>
#include <stdio.h>


typedef struct sTreeNode{
    int value;
    struct sTreeNode* left;
    struct sTreeNode* right;
    struct sTreeNode* parent;
} TreeNode;


TreeNode* create_edge_node(int value, TreeNode* parent_p){
    TreeNode* node_p = (TreeNode*)malloc(sizeof(TreeNode));
    node_p->value = value;
    node_p->left = node_p->right = NULL;
    node_p->parent = parent_p;
    return node_p;
}

TreeNode* create_tree(int value){
    return create_edge_node(value, NULL);
}

void insert_value(TreeNode* root_p, int value){
    TreeNode* new_root_p = root_p;
    TreeNode* not_null_tmp_p = root_p;
    while (new_root_p != NULL){
        if (value < new_root_p->value){
            not_null_tmp_p = new_root_p;
            new_root_p = new_root_p->left;
        }
        else if (value > new_root_p->value){
            not_null_tmp_p = new_root_p;
            new_root_p = new_root_p->right;
        }
        else return;
    }
    if (value > not_null_tmp_p->value){
        not_null_tmp_p->right = create_edge_node(value, not_null_tmp_p);
    }
    else if (value < not_null_tmp_p->value){
        not_null_tmp_p->left = create_edge_node(value, not_null_tmp_p);
    }
}

TreeNode* search_value(TreeNode* root_p, int value){
    TreeNode* new_root_p = root_p;
    while (new_root_p != NULL){
        if (new_root_p->value > value){
            new_root_p = new_root_p->left;
        }
        else if(new_root_p->value < value){
            new_root_p = new_root_p->right;
        }
        else return new_root_p;
    }
    return NULL;
}

void remove_value(TreeNode* root_p, int value){
    TreeNode* target_node_p = search_value(root_p, value);
    if (target_node_p == NULL) return;
    if (target_node_p->right == NULL && target_node_p->left == NULL){
        if (target_node_p->parent != NULL){
            if (target_node_p->parent->left == target_node_p){
                target_node_p->parent->left = NULL;
            }
            else{
                target_node_p->parent->right = NULL;
            }
        else{
            root_p = NULL;
        }
        free(target_node_p);
        return;
        }
    }
    if (target_node_p->right == NULL){
        if (target_node_p->parent != NULL){
            if (target_node_p->parent->left == target_node_p){
                target_node_p->parent->left = target_node_p->left;
            }
            else{
                target_node_p->parent->right = target_node_p->left;
            }
        else{
            root_p = target_node_p->left;
            root_p->parent = NULL;
        }
        free(target_node_p);
        return;
    }
    if (target_node_p->left == NULL){
        if (target_node_p->parent != NULL){
            if (target_node_p->parent->left == target_node_p){
                target_node_p->parent->left = target_node_p->right;
            }
            else{
                target_node_p->parent->right = target_node_p->right;
            }
        else{
            root_p = target_node_p->right;
            root_p->parent = NULL;
        }
        free(target_node_p);
        return;
    }
    }
    TreeNode* tmp_p = target_node_p->right;
    while(tmp_p != NULL && tmp_p->left != NULL){
        tmp_p = tmp_p->left;
    }
    if (tmp_p == target_node_p->right){
        target_node_p->right = NULL;
        target_node_p->value = tmp_p->value;
        free(tmp_p);
        return;
    }
    tmp_p->parent->left = NULL;
    target_node_p->value = tmp_p->value;
    free(tmp_p);
}


void print_tree_inorder(TreeNode* root_p){
    TreeNode* prev = NULL;
    TreeNode* current_p = root_p;
    while (current_p != NULL){
        printf("New iteration: %d\n", current_p->value);
        if (prev == current_p->parent){
            if(current_p->left != NULL) {
                prev = current_p;
                current_p = current_p->left;
                continue;
            }
        }

        printf("Current: %d\n", current_p->value);

        if (prev == current_p->left || prev == current_p->parent){
            if(current_p->right != NULL) {
                prev = current_p;
                current_p = current_p->right;
                continue;
            }
        }

        prev = current_p;
        current_p = current_p->parent;
    }
    printf("\n");
}

void delete_tree(TreeNode* root_p){
    TreeNode* prev = NULL;
    TreeNode* current_p = root_p;
    while (current_p != NULL){
        if (prev == current_p->parent){
            if(current_p->left != NULL) {
                prev = current_p;
                current_p = current_p->left;
                continue;
            }
        }

        if (prev == current_p->left || prev == current_p->parent){
            if(current_p->right != NULL) {
                prev = current_p;
                current_p = current_p->right;
                continue;
            }
        }
        printf("%d\t", current_p->value);
        prev = current_p;
        current_p = current_p->parent;
    }
    printf("\n");
}



int main(){
    TreeNode* root_p = create_tree(10);
    insert_value(root_p, 1);
    insert_value(root_p, 15);

    insert_value(root_p, 7);

    insert_value(root_p, 2);
    insert_value(root_p, 0);

    print_tree_inorder(root_p);
    printf("%d\n", root_p->left->left->value);
    printf("%d\n", root_p->left->right->left->value);
    printf("%d\n", root_p->left->right->value);
    printf("%d\n", root_p->right->value);
    printf("%d\n", root_p->left->value);
    system("pause");
}