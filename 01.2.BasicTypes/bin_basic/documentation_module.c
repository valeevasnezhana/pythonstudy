#include <stdarg.h>
#include <stdlib.h>
#include "documentation_module.h"

int validate(char* data) {
    int validation_result = !strcmp(data, Available_document);
    return validation_result;
}

int* check_available_documentation_module(int (*validate) (char*), int document_count, ...) {
    int* availability_array = (int*) malloc(Max_documents_count*sizeof(int));
    for (int i = 0; i < Max_documents_count; i++) {
        availability_array[i] = 0;
    }

    va_list valist;
    va_start(valist, document_count);
    for (int i = 0; i < document_count; i++) {
        char* document = va_arg(valist, char*);
        int validation_result = validate(document);
        availability_array[i] = validation_result;  
    }
    va_end(valist);

    return availability_array;
}
