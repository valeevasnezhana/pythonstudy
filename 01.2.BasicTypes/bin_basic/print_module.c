#include <stdio.h>
#include <time.h>

#include "print_module.h"

char print_char(char ch) {
    return putchar(ch);
}

void print_string(char (*print) (char), char* message) {
    char* current_char_ptr = message;
    while (*current_char_ptr != '\0') {
        print(*current_char_ptr);
        current_char_ptr++;
    }
}

void print_log(char (*print) (char), char* message) {
    time_t time_info;
    time(&time_info);

    struct tm* local_time_info;
    local_time_info = localtime(&time_info);
    char time_string_buffer[128];
    strftime(time_string_buffer, 128, "%H:%M:%S", local_time_info);

    print_string(print, "[LOG] ");
    print_string(print, time_string_buffer);
    print_string(print, " ");
    print_string(print, message);
    print_string(print, "\n");
}