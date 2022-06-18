import typing as tp


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    common_types = [bool, int, float, str, list]
    result_type: list[tp.Any] = []
    for value in data:
        if value == 1:
            result_type.append(bool)
        elif value is False:
            result_type.append(bool)
        elif value is 0:
            result_type.append(0)
        elif value:
            if type(value) == tuple:
                result_type.append(list)
            else:
                result_type.append(type(value))
        else:
            result_type.append('')
    m = -1
    for i in range(len(common_types)):
        if common_types[i] in result_type:
            m = i
    if m >= 0:
        common_type = common_types[m]
    else:
        if 0 in result_type:
            return [0] * len(data)
        else:
            return [""] * len(data)
    result_list: list[tp.Any] = []
    for value in data:
        if common_type == bool:
            if value:
                result_list.append(True)
            else:
                result_list.append(False)
        if common_type == int:
            if value:
                result_list.append(int(value))
            else:
                result_list.append(0)
        if common_type == float:
            if value:
                result_list.append(float(value))
            else:
                result_list.append(0.0)
        if common_type == str:
            if value:
                result_list.append(value)
            else:
                result_list.append("")
        if common_type == list:
            if value:
                if (type(value) == list) or (type(value) == tuple):
                    result_list.append(list(value))
                else:
                    result_list.append([value])
            else:
                result_list.append([])
    return result_list
