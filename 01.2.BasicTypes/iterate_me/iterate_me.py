import typing as tp


def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    # squares_list: list[int] = []
    # for value in elements:
    #     squares_list.append(value ** 2)
    # return squares_list
    return [v**2 for v in elements]


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    # indices_from_one: list[int] = []
    # for counter in range(1, len(elements) + 1):
    #     indices_from_one.append(counter)
    # return indices_from_one
    return list(range(1, len(elements) + 1))


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    max_element_index: tp.Optional[int] = None
    if len(elements) != 0:
        max_element = float('-inf')
        for index, value in enumerate(elements):
            if value > max_element:
                max_element_index = index
                max_element = value
    return max_element_index


# ====================================================================================================

def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    # every_second_element_lst: list[int] = []
    # for index, val in enumerate(elements):
    #     if index % 2 == 1:
    #         every_second_element_lst.append(val)
    # return every_second_element_lst
    return [val for index, val in enumerate(elements) if index % 2 == 1]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    for index, value in enumerate(elements):
        if value == 3:
            return index
    return None


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    last_three_index: tp.Optional[int] = None
    for index, value in reversed(list(enumerate(elements))):
        if value == 3:
            last_three_index = index
            break
    return last_three_index


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    # list_sum: int = 0
    # if elements:
    #     list_sum = sum(elements)
    return sum(elements)

    # ====================================================================================================


def get_min_max(elements: list[int], default: tp.Optional[int]) -> tuple[tp.Optional[int], tp.Optional[int]]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    list_min: tp.Optional[int] = default
    list_max: tp.Optional[int] = default
    if elements:
        list_min = min(elements)
        list_max = max(elements)
    return list_min, list_max


# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return result if (result := elements[i]) > boundary else None
