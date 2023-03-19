Checking full_computation.c ...
full_computation.c:39:16: style: The scope of the variable 'x_value' can be reduced. [variableScope]
        double x_value;
               ^
full_computation.c:30:28: style: Parameter 'x_array' can be declared with const [constParameter]
int create_y_array(double* x_array, double** y_array, int array_size, char* input_string) {
                           ^
1/9 files checked 13% done
Checking full_computation_main.c ...
full_computation_main.c:16:5: warning: scanf() without field width limits can crash with huge input data. [invalidscanf]
    scanf("%s %lf", input_string, &x_value);
    ^
2/9 files checked 16% done
Checking graph.c ...
graph.c:21:27: style: Parameter 'y_array' can be declared with const [constParameter]
void print_result(double* y_array) {
                          ^
3/9 files checked 21% done
Checking main_module_entry_point.c ...
main_module_entry_point.c:21:5: warning: scanf() without field width limits can crash with huge input data. [invalidscanf]
    scanf("%s", input_string);
    ^
4/9 files checked 24% done
Checking numeric_stack.c ...
5/9 files checked 30% done
Checking shunting_yard_algo.c ...
6/9 files checked 53% done
Checking stack.c ...
7/9 files checked 59% done
Checking token_computation.c ...
token_computation.c:64:24: style: Local variable 'output_value' shadows outer argument [shadowArgument]
                double output_value;
                       ^
token_computation.c:22:43: note: Shadowed declaration
                                  double* output_value) {
                                          ^
token_computation.c:64:24: note: Shadow variable
                double output_value;
                       ^
token_computation.c:113:24: style: Local variable 'output_value' shadows outer argument [shadowArgument]
                double output_value;
                       ^
token_computation.c:22:43: note: Shadowed declaration
                                  double* output_value) {
                                          ^
token_computation.c:113:24: note: Shadow variable
                double output_value;
                       ^
8/9 files checked 84% done
Checking tokenizer.c ...
tokenizer.c:87:33: style: Expression is always false because 'else if' condition matches previous condition at line 81. [multiCondition]
        } else if (current_char == ' ') {
                                ^
9/9 files checked 100% done
token_computation.c:11:0: style: The function 'print_numeric_stack_state' is never used. [unusedFunction]

^
shunting_yard_algo.c:21:0: style: The function 'print_output_queue_state' is never used. [unusedFunction]

^
shunting_yard_algo.c:11:0: style: The function 'print_stack_state' is never used. [unusedFunction]

^
gruntmet@ga-b3 src % 
