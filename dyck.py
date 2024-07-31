from collections import deque
from typing import Optional
from ordered_tree import OrderedNode, ordered_add_parents
from permutation import fischer_yates


'''
An 'x-augmented Dyck path' is a word in x and y
that starts with x and is then follwoed by a 
Dyck path.  
'''


def dyck_rotate(w: list[str]) -> list[str]:
    '''Rotates word to an x-augmented Dyck path.
    '''
    if w.count('x') - 1 != w.count('y'):
        raise ValueError('Input must have one more x than y.')

    N = len(w)
    dq = deque(w)

    height = 0
    w_index = 0
    dq_index = 0

    while dq_index != N:
        if w[w_index] == 'x':
            height += 1
        elif w[w_index] == 'y':
            height -= 1
        w_index += 1
        w_index %= N
        dq_index += 1
        if height < 1:
            # Reset.
            for _ in range(dq_index):
                dq.append(dq.popleft())
            dq_index = 0
            height = 0
    return list(dq)


def is_dyck(w: list[str]) -> bool:
    '''Checks the input is a Dyck path.
    '''
    wx = w.count('x')
    wy = w.count('y')
    N = len(w)

    if wx != wy or wx + wy != N:
        return False

    height = 0
    for c in w:
        if c == 'x':
            height += 1
        elif c == 'y':
            height -= 1
        if height < 0:
            return False
    return True


def random_dyck(N: int) -> list[str]:
    '''Randomly sampled x-augmented Dyck path of length N.
    '''
    if N % 2 != 1:
        raise ValueError("Input must be odd.")

    w = fischer_yates(['x' for _ in range((N // 2) + 1)] +
                      ['y' for _ in range(N // 2)],
                      in_place=True)
    return dyck_rotate(w)


def dyck_to_ordered_tree(w: list[str]) -> OrderedNode:
    '''Converts x-augmented Dyck path to an ordered tree. 
    '''

    # Left and right inclusive.
    def construct_tree(left, right):
        if left == right:
            return OrderedNode()

        current_root = OrderedNode()

        index = left
        height_last_index = {}
        current_height = 0
        k = 0  # After for loop - height of last x.

        for c in w[left: right + 1]:
            if c == 'x':
                k = current_height
                current_height += 1
                height_last_index[current_height] = index
            elif c == 'y':
                current_height -= 1
            index += 1

        indices = list(height_last_index.values())[:k+1]

        # Using that the dict keys are in insertion order (height order).
        current_root.children = [construct_tree(i1, i2-1)
                                 for i1, i2 in zip(indices,
                                                   indices[1:])]
        return current_root

    N = len(w)
    root = construct_tree(0, N - 1)

    # Add parent pointers.
    return ordered_add_parents(root)


def dyck_random_ordered_tree(N: int) -> Optional[OrderedNode]:
    '''Uniformly generates a random N node ordered tree.

    A tree is ordered if the children of each node have an 
    ordering.  This algorithm uses Fischer-Yates to get a 
    random word with an equal number of x's and y's,
    rotates it to get a (unique) Dyck path, and then uses
    the bijection from Dyck paths to ordered trees to get an
    ordered tree.  
    '''
    if N == 0:
        return None
    w = ['x'] + random_dyck(2*(N-1))
    return dyck_to_ordered_tree(w)
