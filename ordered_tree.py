
from typing import Optional
from binary_tree import BinaryNode, random_binary_tree


class OrderedNode:
    def __init__(self, children: Optional[list] = None, parent=None):
        self.children = [] if children is None else children
        self.parent = parent


def ordered_add_parents(root: OrderedNode) -> OrderedNode:
    '''Adds aprent pointers.
    '''
    nodes = [root]
    while len(nodes) > 0:
        new_nodes = []
        for node in nodes:
            for child in node.children:
                new_nodes.append(child)
                child.parent = node
        nodes = new_nodes
    return root


def binary_tree_to_ordered_tree(root: BinaryNode) -> OrderedNode:
    '''Converts a binary tree into an ordered tree with one more node.

    Follows the inverse of the LC-RS transformation.  
    '''
    # Get the rows.
    bin_rows = []
    new_root = BinaryNode(left=root)
    bin_rows.append([new_root])
    root.parent = new_root

    current_row = []
    while root is not None:
        current_row.append(root)
        root = root.right

    while len(current_row) > 0:
        bin_rows.append(current_row)
        new_row = []

        for node in current_row:
            if node.left is not None:
                child = node.left
                while child is not None:
                    new_row.append(child)
                    child = child.right

        current_row = new_row

    # Make the new nodes.
    ordered_rows = []
    for bin_row in bin_rows:
        ordered_rows.append([OrderedNode()
                             for _ in range(len(bin_row))])

    # Make the new node child connections.
    for current_bin_row,  \
            current_ordered_row, \
            next_ordered_row in zip(bin_rows, ordered_rows, ordered_rows[1:]):

        next_index = 0
        for current_index, current_node in enumerate(current_bin_row):
            if current_node.left is not None:
                current_node = current_node.left
                while current_node is not None:
                    current_ordered_row[current_index].children.append(
                        next_ordered_row[next_index])
                    next_index += 1
                    current_node = current_node.right

    # Make the parent connections.
    ordered_root = ordered_rows[0][0]
    return ordered_add_parents(ordered_root)


def random_ordered_tree(N: int) -> Optional[OrderedNode]:
    '''Uniformly generates a random N node ordered tree.

    A tree is ordered if the children of each node have an 
    ordering.  This algorithm uses Remy's algorithm to 
    generate a random binary tree and then uses a bijection 
    between binary and ordered trees to obtain the result.  
    '''

    if N == 0:
        return None
    binary_tree = random_binary_tree(N - 1)
    return binary_tree_to_ordered_tree(binary_tree)


def ordered_tree_to_dyck(root: OrderedNode) -> str:
    '''Converts an ordered tree to leading x Dyck path.

    Used for tree serialization.  Output word is a word 
    in the letters x and y.  The initial letter is an x
    and after that the rest of the string is a Dyck path.  
    '''
    res = []

    def dfs(node):
        if node is None:
            return
        for child in node.children:
            dfs(child)
        res.append('x' + 'y'*len(node.children))

    dfs(root)
    return ''.join(res)
