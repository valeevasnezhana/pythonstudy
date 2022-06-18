import typing as tp


def get_fizz_buzz(n: int) -> list[tp.Union[int, str]]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    fizz_buzz_list: tp.List[tp.Union[int, str]] = []
    for i in range(1, n + 1):
        fizz_buzz_list.append(i)
        if i % 15 == 0:
            fizz_buzz_list[i - 1] = "FizzBuzz"
        elif i % 3 == 0:
            fizz_buzz_list[i - 1] = "Fizz"
        elif i % 5 == 0:
            fizz_buzz_list[i - 1] = "Buzz"
    return fizz_buzz_list

