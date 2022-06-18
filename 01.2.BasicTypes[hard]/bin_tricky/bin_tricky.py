import typing as tp


def find_median(nums1: tp.Union[list[int], range], nums2: tp.Union[list[int], range]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    param nums1: sorted sequence of integers
    param nums2: sorted sequence of integers
    return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    start = 0
    end = len(nums1)
    len1 = len(nums1)
    len2 = len(nums2)
    while start <= end:

        i = (start + end) // 2
        j = (len1 + len2 + 1) // 2 - i

        down_med1 = float('-inf') if i == 0 else nums1[i - 1]
        up_med1 = float('inf') if i == len1 else nums1[i]

        down_med2 = float('-inf') if j == 0 else nums2[j - 1]
        up_med2 = float('inf') if j == len2 else nums2[j]

        if down_med2 > up_med1:
            start = i + 1
        elif down_med1 > up_med2:
            end = i - 1

        else:
            if (len1 + len2) % 2 == 0:
                median = (max(down_med1, down_med2) + min(up_med1, up_med2)) / 2
            else:
                median = max(down_med1, down_med2)
            return float(median)

    assert False, "Not reachable"
