import typing as tp


def find_median(nums1: tp.Union[list[int], range], nums2: tp.Union[list[int], range]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    param nums1: sorted sequence of integers
    param nums2: sorted sequence of integers
    return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    n = len(nums1)
    m = len(nums2)
    i = 0
    j = 0
    mid1, mid2 = -1, -1

    for count in range(((n + m) // 2) + 1):
        if (m + n) % 2 == 0:
            mid2 = mid1
        if i != n and j != m:
            if nums1[i] > nums2[j]:
                mid1 = nums2[j]
                j += 1
            else:
                mid1 = nums1[i]
                i += 1
        elif (i < n):
            mid1 = nums1[i]
            i += 1

            # for case when j<m,
        else:
            mid1 = nums2[j]
            j += 1
    if (m + n) % 2 == 1:
        return float(mid1)
    else:
        return float((mid1 + mid2) / 2)



