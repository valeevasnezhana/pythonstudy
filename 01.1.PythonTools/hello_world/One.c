#include <stdio.h>

long long get_whole_of_division(long long nominator, long long divisor) {
    long long whole = 0;
    long long current_value = nominator;
    while (current_value >= divisor) {
        whole = whole + 1;
        current_value = current_value - divisor;
    }
    return whole;
}

long long create_largest_divisor(long long input_value) {
    if (input_value < 0) {
        return -1;
    }
    // тут надо решить что надо возвращать для 0
    if (input_value == 0) {
        return -1;
    }
    if (input_value == 1) {
        return 1;
    }

    long long iteration = 0;
    long long current_value = input_value;
    long long current_divisor = 2;

    long long largest_successful_divisor = -1;

    while (current_value > 1) {
//        printf("Iter: %d. Value: %d, divisor: %d\n", iteration, current_value, current_divisor);
        long long whole = get_whole_of_division(current_value, current_divisor);
        long long remainder = current_value - current_divisor * whole;
//        printf("Whole: %d. remainder: %d\n", whole, remainder);
        if (remainder == 0) {
            largest_successful_divisor = current_divisor;
            current_value = whole;
        } else {
//            printf("%d is not divided by %d\n", current_value, current_divisor);
            current_divisor++;
        }
        iteration++;
    }
    return largest_successful_divisor;
}

void print_largest_divisor(long long input_value) {
    long long largest_divisor = create_largest_divisor(input_value);
    if (largest_divisor > 0) {
        printf("%lld\n", largest_divisor);
    } else {
        printf("n/a\n");
    }
}

int main(int argc, char* argv[]) {
    long long input_value;
    scanf("%lld", &input_value);
    print_largest_divisor(input_value);
}
