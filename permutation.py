from math import floor
from random import uniform

# Built-in way to do this is to use random.shuffle(nums).


def fischer_yates(nums: list, in_place=False) -> list:
    '''Fischer-Yates algorithm for random permutation.

    Returns a uniformly randomly sampled permutation of 
    the input array.  This is done either in place or 
    not depending on the optional argument.  
    '''
    if in_place:
        nums = nums.copy()
    N = len(nums)
    for i in range(N):
        index = floor(uniform(i, N))
        nums[i], nums[index] = nums[index], nums[i]
    return nums
