#ifndef DOOR_STRUCT_H
#define DOOR_STRUCT_H

struct door {
  int id;
  int status;
};

void initialize_doors(struct door* doors);
void set_status_door(struct door* doors, int status);
void door_sort(struct door* doors);
void door_swap(struct door* doors, int i, int j);
void door_output(struct door* doors);

#endif