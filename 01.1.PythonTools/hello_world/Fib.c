#include <stdio.h>

long long create_nth_fibonacci_number(long long n) {
    if (n == 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    return create_nth_fibonacci_number(n - 1) + create_nth_fibonacci_number(n - 2);
}

int main(int argc, char* argv[]) {
    long long input_number;
    scanf("%lld", &input_number);
    long long result = create_nth_fibonacci_number(input_number);
    printf("%lld\n", result);
}
