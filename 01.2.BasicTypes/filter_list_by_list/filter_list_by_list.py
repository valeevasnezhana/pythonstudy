import typing as tp


def filter_list_by_list(lst_a: tp.Union[list[int], range], lst_b: tp.Union[list[int], range]) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    if len(lst_a) == 0 or len(lst_b) == 0:
        return lst_a
    result: list[int] = []
    id1, id2 = 0, 0
    while id1 < len(lst_a) and id2 < len(lst_b):
        if lst_a[id1] < lst_b[id2]:
            result.append(lst_a[id1])
            id1 += 1
        elif lst_a[id1] > lst_b[id2]:
            id2 += 1
        else:
            id1 += 1
            id2 += 1
    while id1 < len(lst_a):
        result.append(lst_a[id1])
        id1 += 1
    return result



