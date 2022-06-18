def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    # range, range -> tuple
    if type1 == range and type2 == range:
        return tuple
    # only not iterative
    non_iterative = [bool, int, float, complex]
    for i in range(len(non_iterative)):
        if type1 == non_iterative[i]:
            for j in range(len(non_iterative)):
                if type2 == non_iterative[j]:
                    return non_iterative[max(i, j)]
    # only iterative,
    # but range, range -> tuple, taken above
    # but str, any type -> str, taken below
    iterative = [range, tuple, list]  # range < tuple < list
    for i in range(len(iterative)):
        if type1 == iterative[i]:
            for j in range(len(iterative)):
                if type2 == iterative[j]:
                    return iterative[max(i, j)]
    # str + any type -> str
    statement1 = str in (type1, type2)
    # iterative + not iterative -> str
    statement2 = (type1 in iterative) and (type2 in non_iterative)
    statement3 = (type1 in non_iterative) and (type2 in iterative)
    assert (statement1 or statement2 or statement3), "no solution"
    return str

