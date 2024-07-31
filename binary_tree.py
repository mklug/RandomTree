from typing import Optional
import random


class BinaryNode:
    def __init__(self, left=None, right=None, parent=None):
        self.left = left
        self.right = right
        self.parent = parent


def random_extended_binary_tree(N_internal: int) -> BinaryNode:
    '''Remy's algorithm for a random extended binary tree.

    Remy's linear-time algorithm for constructing a uniformly-sampled
    random extended binary tree.  A binary tree is extended if all 
    node either have two non-null children, or they are leaves.  
    '''

    if not 0 <= N_internal:
        raise ValueError("Must have a nonnegative number of interal nodes.")

    if N_internal == 0:
        return BinaryNode()

    LEFT, RIGHT = 0, 1
    nodes = [BinaryNode()]

    while N_internal > 0:
        random_node = random.choice(nodes)
        parent = random_node.parent
        # direction to add new leaf.
        random_direction = random.randint(0, 1)

        # Create new node.
        new_leaf = BinaryNode()
        if random_direction == LEFT:
            new_node = BinaryNode(left=new_leaf,
                                  right=random_node,
                                  parent=parent)
        elif random_direction == RIGHT:
            new_node = BinaryNode(left=random_node,
                                  right=new_leaf,
                                  parent=parent)
        new_leaf.parent = new_node
        nodes.append(new_leaf)
        nodes.append(new_node)

        # Fix parent node
        if parent is not None:
            if parent.left == random_node:
                parent.left = new_node
            elif parent.right == random_node:
                parent.right = new_node

        # Fix random node.
        random_node.parent = new_node

        N_internal -= 1

    # Find the root to return.
    node = nodes[0]
    while node.parent is not None:
        node = node.parent
    return node


def is_leaf(node: BinaryNode) -> bool:
    '''Checks if the input node is a leaf.
    '''
    return node.left is None and node.right is None


def leaf_prune(root: BinaryNode) -> Optional[BinaryNode]:
    '''Explores the tree with DFS and removes leaves.
    '''
    def dfs(node: Optional[BinaryNode]) -> None:
        if node is None:
            return
        if is_leaf(node):
            parent = node.parent
            if parent is not None:
                if parent.left == node:
                    parent.left = None
                elif parent.right == node:
                    parent.right = None
        dfs(node.left)
        dfs(node.right)

    if is_leaf(root):
        return None
    dfs(root)
    return root


def random_binary_tree(N: int) -> Optional[BinaryNode]:
    '''Uniformly samples from binary trees with N nodes.

    Uses Remy's method to generate an extended binary 
    tree with N internal nodes and then prunes the leaves.  
    '''
    if not 0 <= N:
        raise ValueError("Tree cannot have a negative number of nodes.")

    root_extended = random_extended_binary_tree(N)
    root = leaf_prune(root_extended)
    return root
