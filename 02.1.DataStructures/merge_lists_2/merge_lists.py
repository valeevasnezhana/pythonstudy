import typing as tp
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    heap: list[tuple[int, int, int]] = []
    merged_list: list[int] = []
    for list_id, list_ in enumerate(seq):
        if list_:
            value = list_[0]
            heapq.heappush(heap, (value, list_id, 0))
    while heap:
        value, list_id, el_id = heapq.heappop(heap)
        merged_list.append(value)
        if el_id < len(seq[list_id]) - 1:
            el_id += 1
            value = seq[list_id][el_id]
            heapq.heappush(heap, (value, list_id, el_id))
    return merged_list
