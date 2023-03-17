typedef struct s_t_btree{
    int item;
    struct s_t_btree* left;
    struct s_t_btree* right;
    struct s_t_btree* parent;
} t_btree;

t_btree* bstree_create_node(int item);

void bstree_insert(t_btree *root, int item, int (*cmpf) (int, int));

void bstree_apply_infix(t_btree *root, void (*applyf) (int));

void bstree_apply_prefix(t_btree *root, void (*applyf) (int));

void bstree_apply_postfix(t_btree *root, void (*applyf) (int));
