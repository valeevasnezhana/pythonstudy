#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stack.h"
#include "token.h"
#include "shunting_yard_algo.h"

void print_stack_state(struct stack* operator_stack) {
    struct stack_node* current_node = operator_stack->head;
    printf("# Stack: ");
    while (current_node != NULL) {
        printf("[%s]", current_node->token_p->string_value);
        current_node = current_node->next;
    }
    printf("\n");
}

void print_output_queue_state(struct token* output_token_array, int array_size) {
    printf("# Output: ");
    for (int i = 0; i < array_size; i++) {
        printf("[%s]", output_token_array[i].string_value);
    }
    printf("\n");
}

void move_token_from_stack_to_output(struct token* output_token_array, struct stack* operator_stack, int* output_token_index) {
    struct token* token_from_stack = pop(operator_stack);
    output_token_array[(*output_token_index)++] = (*token_from_stack);
//    printf("Moved token from stack to output: %s\n", token_from_stack->string_value);
}

int get_binary_operation_importance(char* operation_string_value) {
    if (strcmp(operation_string_value, "+") == 0 || strcmp(operation_string_value, "-") == 0) {
        return 1;
    } else if (strcmp(operation_string_value, "*") == 0 || strcmp(operation_string_value, "/") == 0) {
        return 2;
    } else {
        return -1;
    }
}

int apply_shunting_yard_algo(struct token* input_token_array, int input_token_amount, struct token** output_token_array, int* output_token_amount) {
    int incorrect_input_tokens = 0;

    (*output_token_array) = (struct token*) malloc(input_token_amount * sizeof(struct token));
    int output_token_index = 0;

//    printf("\n----- START PARSING TOKENS -----\n");
    struct token* current_token = NULL;
    struct token* token_from_stack = NULL;
    struct stack* operator_stack = init();
    for (int input_token_index = 0; input_token_index < input_token_amount; input_token_index++) {
        current_token = &input_token_array[input_token_index];
//        printf("+++ [%d, %d]: %s\n", input_token_index, current_token->type, current_token->string_value);
        if (current_token->type == NUMBER) {
//            printf("Number added to output: %s\n", current_token->string_value);
            (*output_token_array)[output_token_index++] = (*current_token);
        } else if (current_token->type == BINARY_OPERATION) {
            int current_operation_importance = get_binary_operation_importance(current_token->string_value);
            while (top(operator_stack) != NULL && top(operator_stack)->type == BINARY_OPERATION) {
                token_from_stack = top(operator_stack);
//                printf("Retrieved token from stack: %s\n", token_from_stack->string_value);
                int stack_operation_importance = get_binary_operation_importance(token_from_stack->string_value);
                if (current_operation_importance <= stack_operation_importance) {
                    move_token_from_stack_to_output((*output_token_array), operator_stack, &output_token_index);
                } else {
                    break;
                }
            }
            push(operator_stack, current_token);
        } else if (current_token->type == FUNCTION || current_token->type == UNARY_OPERATION) {
//            printf("Function added to stack\n");
            push(operator_stack, current_token);
        } else if (current_token->type == LEFT_BRACE) {
//            printf("Left brace added to stack\n");
            push(operator_stack, current_token);
        } else if (current_token->type == RIGHT_BRACE) {
//            printf("Right brace added to stack\n");
            while (top(operator_stack) != NULL && top(operator_stack)->type != LEFT_BRACE) {
                move_token_from_stack_to_output((*output_token_array), operator_stack, &output_token_index);
            }
            if (top(operator_stack) == NULL || top(operator_stack)->type != LEFT_BRACE) {
                incorrect_input_tokens = 1;
                free(current_token->string_value);
                break;
            } else {
                token_from_stack = pop(operator_stack);
                free(token_from_stack->string_value);

                if (top(operator_stack) != NULL && (current_token->type == FUNCTION || current_token->type == UNARY_OPERATION)) {
                    move_token_from_stack_to_output((*output_token_array), operator_stack, &output_token_index);
                }
                free(current_token->string_value);
            }
        }
//        printf("\n");
//        print_stack_state(operator_stack);
//        print_output_queue_state((*output_token_array), output_token_index);
//        printf("\n");
    }

    while (top(operator_stack) != NULL) {
        if (top(operator_stack)->type == LEFT_BRACE || top(operator_stack)->type == RIGHT_BRACE) {
            incorrect_input_tokens = 1;
            break;
        }
        move_token_from_stack_to_output((*output_token_array), operator_stack, &output_token_index);
    }

    *output_token_amount = output_token_index;
    destroy(operator_stack);
//    printf("\nFINAL STATE SHUNT:\n");
//    print_stack_state(operator_stack);
//    print_output_queue_state((*output_token_array), output_token_index);
//    printf("\n");
    return incorrect_input_tokens;
}