import typing as tp


def find_value(nums: tp.Union[list[int], range], value: int) -> bool:
    """
    Find value in sorted sequence
    :param nums: sequence of integers. Could be empty
    :param value: integer to find
    :return: True if value exists, False otherwise
    """
    if not nums:
        return False
    
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] == value:
            return True
        elif nums[mid] < value:
            left = mid + 1
        else:
            right = mid
    if left == len(nums) - 1 and nums[left] == value:
        return True
    return False
    

