#include <stdio.h>

#include "print_module.h"
#include "documentation_module.h"
#include <stdlib.h>

int main() {
    print_log(print_char, "Module_load_successb");
    int* availability_mask = check_available_documentation_module(validate, Documents_count, Documents);
	for (int i = 0; i < Documents_count; i++) {
        if (availability_mask[i] == 0) {
            printf("[название документа : unavailable]\n");
        } else {
            printf("[название документа : available]\n");
        }
    }
    free(availability_mask);
    return 0;
}
