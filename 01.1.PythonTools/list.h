#ifndef LIST_H
#define LIST_H
#include "door_struct.h"

struct node {
  struct door* door_inst;
  struct node* next;
};

struct node* init(struct door* door_instance);
struct node* add_door(struct node* lst_elem, struct door* door_instance);
struct node* find_door(int door_id, struct node* root);
struct node* remove_door(const struct node*  lst_elem, struct node* root);
void destroy(struct node* root);
void list_output(struct node* root);
int list_len(struct node* root);
void door_init(struct door* door_instance, int door_id, int status);

#endif
