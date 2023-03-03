#include <stdio.h>

int encode_char_into_single_hex(int input_char) {
    if (input_char < 10) {
        return '0'+input_char;
    } else {
        return 'A'+(input_char-10);
    }
}

void encode_letter_into_two_digit_hex_and_print(int input_letter_char) {
    int first_symbol = input_letter_char / 16;
    int second_symbol = input_letter_char % 16;
    printf("%c%c", encode_char_into_single_hex(first_symbol), encode_char_into_single_hex(second_symbol));
}

int decode_single_hex_into_value(int input_hex_char) {
    if (input_hex_char >= 'A' && input_hex_char <= 'F') {
        return (input_hex_char - 'A') + 10;
    } else {
        return input_hex_char - '0';
    }
}

void decode_two_hex_digits_into_letter_and_print(int first_digit, int second_digit) {
    int first_value = decode_single_hex_into_value(first_digit);
    int second_value = decode_single_hex_into_value(second_digit);
    int output_value = first_value*16 + second_value;
    printf("%c", output_value);
}

int main(int argc, char* argv[]) {
    if (argc != 2){
        printf("n/a\n");
        return 0;
    }
    int input_mode;
    char tail_char;
    int part_amount = sscanf(argv[1], "%d%s", &input_mode, &tail_char);
    if (part_amount != 1) {
        printf("n/a\n");
        return 0;
    }
    if (input_mode != 0 && input_mode != 1) {
        printf("n/a\n");
    }


    if (input_mode == 0) {
        int iteration = 0;
        int previous_char = -1;
        int current_char = -1;

        while (current_char != '\n') {
            iteration++;
            previous_char = current_char;
            current_char = getchar();

            if (previous_char != ' ' && !(current_char == ' ' || current_char == '\n') && iteration > 1) {
                printf("n/a");
                break;
            } else if (previous_char != ' ' && (current_char == ' ' || current_char == '\n')) {
                if (iteration > 2) {
                    printf(" ");
                }
                encode_letter_into_two_digit_hex_and_print(previous_char);
            }

            if (current_char == '\n') {
                break;
            }
        }
        printf("\n");
    } else if (input_mode == 1) {
        int iteration = 0;
        int before_previous_char = -1;
        int previous_char = -1;
        int current_char = -1;

        while (current_char != '\n') {
            iteration++;
            before_previous_char = previous_char;
            previous_char = current_char;
            current_char = getchar();

            if (before_previous_char != ' ' && previous_char != ' ' && !(current_char == ' ' || current_char == '\n') && iteration > 2) {
                printf("n/a");
                break;
            } else if (before_previous_char != ' ' && previous_char != ' ' && (current_char == ' ' || current_char == '\n')) {
                if (iteration > 3) {
                    printf(" ");
                }
                decode_two_hex_digits_into_letter_and_print(before_previous_char, previous_char);
            }

            if (current_char == '\n') {
                break;
            }
        }
        printf("\n");
    } else {
        printf("n/a\n");
    }
    return 0;
}
