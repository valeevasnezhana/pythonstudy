#include "list.h"

#include <stdio.h>
#include <stdlib.h>

#include "door_struct.h"

struct node* init(struct door* door_instance) {
  struct node* new_node = NULL;
  if (door_instance != NULL) {
    new_node = malloc(sizeof(struct node));
    new_node->door_inst = door_instance;
    new_node->next = NULL;
  }
  return new_node;
}
struct node* add_door(struct node* lst_elem, struct door* door_instance) {
  struct node* new_node = NULL;
  if (lst_elem != NULL && door_instance != NULL) {
    new_node = init(door_instance);
    new_node->next = lst_elem->next;
    lst_elem->next = new_node;
  }
  return new_node;
}
struct node* find_door(int door_id, struct node* root) {
  struct node* search = root;
  if (root != NULL) {
    while (search != NULL && search->door_inst->id != door_id) {
      search = search->next;
    }
  }
  return search;
}
struct node* remove_door(const struct node* lst_elem, struct node* root) {
  if (root != NULL && lst_elem != NULL) {
    struct node* prev = root;
    struct node* n = root;
    while (n != lst_elem && n != NULL) {
      prev = n;
      n = n->next;
    }
    if (n != NULL) {
      if (n != root) {
        prev->next = n->next;
        free(n);
      } else {
        if (root->next != NULL)
          root = root->next;
        else
          root = NULL;
        free(n);
      }
    }
  }
  return root;
}
void destroy(struct node* root) {
  if (root != NULL) {
    struct node* destroyer = root;

    while (destroyer != NULL) {
      root = root->next;
      free(destroyer);
      destroyer = root;
    }
  }
}

void door_init(struct door* door_instance, int door_id, int status) {
  door_instance->id = door_id;
  door_instance->status = status;
}

void list_output(struct node* root) {
  struct node* runner = root;
  if (root == NULL) printf("List is empty");
  while (runner != NULL) {
    printf("Door_ID:%d\tDoor_STATUS:%d", runner->door_inst->id, runner->door_inst->status);
    runner = runner->next;
    if (runner != NULL) printf("\n");
  }
}

int list_len(struct node* root) {
  int len = 0;
  struct node* runner = root;
  while (runner != NULL) {
    len++;
    runner = runner->next;
  }
  return len;
}