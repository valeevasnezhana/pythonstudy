def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    if not lst_a or not lst_b:
        return lst_a + lst_b
    result_lst: list[int] = []
    index_a, index_b = 0, 0
    while index_a < len(lst_a) and index_b < len(lst_b):
        if lst_a[index_a] <= lst_b[index_b]:
            result_lst.append(lst_a[index_a])
            index_a += 1
        else:
            result_lst.append(lst_b[index_b])
            index_b += 1
    while index_a < len(lst_a):
        result_lst.append(lst_a[index_a])
        index_a += 1
    while index_b < len(lst_b):
        result_lst.append(lst_b[index_b])
        index_b += 1
    return result_lst


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """2
    Merge two sorted lists in one sorted list ising `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    return sorted(lst_a + lst_b)
