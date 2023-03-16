#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "door_struct.h"

#define DOORS_COUNT 15
#define MAX_ID_SEED 10000

int main() {
  struct door doors[DOORS_COUNT];

  initialize_doors(doors);
  door_sort(doors);
  for (int i = 0; i < DOORS_COUNT; i++) {
    set_status_door(&doors[i], 0);
  }
  door_output(doors);
  return 0;
}

// Doors initialization function
// ATTENTION!!!
// DO NOT CHANGE!
void initialize_doors(struct door* doors) {
  srand(time(0));

  int seed = rand() % MAX_ID_SEED;
  for (int i = 0; i < DOORS_COUNT; i++) {
    doors[i].id = (i + seed) % DOORS_COUNT;
    doors[i].status = rand() % 2;
  }
}

void set_status_door(struct door* doors, int status) { doors->status = status; }

void door_sort(struct door* doors) {
  for (int i = 0; i < DOORS_COUNT; i++) {
    for (int j = 0; j < DOORS_COUNT - 1; j++) {
      if (doors[j].id > doors[j + 1].id) {
        struct door tmp = doors[j + 1];
        doors[j + 1] = doors[j];
        doors[j] = tmp;
      }
    }
  }
}

void door_output(struct door* doors) {
  for (int i = 0; i < DOORS_COUNT; i++) {
    printf("%d, %d", doors[i].id, doors[i].status);
    if (i != DOORS_COUNT - 1) printf("\n");
  }
}