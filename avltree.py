'''
Python3 implementation of AVL tree.
AVL tree:
    A kind of binary search tree (BST), which has 2 characteristics:
        1. The difference of depth between its left and right subtrees is no larger than 1;
        2. Its left and right subtrees are also AVL trees.
    Due to this, AVL tree can archive a worst time complexity of O(logN) for search, insert and delete,
    while naive BST has a worst time complexity of O(N) for these operations.
'''


'''
Definition of tree node.
'''
class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = self.right = None
        self.depth = 1


'''
Auxiliary functions
'''
def rightRotation(root: TreeNode) -> TreeNode:
    left = root.left
    subtree = left.right
    root.left = subtree
    left.right = root
    ld = root.left.depth if root.left else 0
    rd = root.right.depth if root.right else 0
    root.depth = max(ld, rd) + 1
    lld = left.left.depth if left.left else 0
    left.depth = max(root.depth, lld) + 1
    return left


def leftRotation(root: TreeNode) -> TreeNode:
    right = root.right
    subtree = right.left
    root.right = subtree
    right.left = root
    ld = root.left.depth if root.left else 0
    rd = root.right.depth if root.right else 0
    root.depth = max(ld, rd) + 1
    rrd = right.right.depth if right.right else 0
    right.depth = max(root.depth, rrd) + 1
    return right


def rebalance(root: TreeNode) -> TreeNode:
    ld = root.left.depth if root.left else 0
    rd = root.right.depth if root.right else 0
    root.depth = max(ld, rd) + 1
    if abs(ld - rd) <= 1:
        return root
    elif ld - rd > 1:
        lld = root.left.left.depth if root.left.left else 0
        lrd = root.left.right.depth if root.left.right else 0
        if lld >= lrd:
            return rightRotation(root)
        else:
            root.left = leftRotation(root.left)
            return rightRotation(root)
    else:
        rld = root.right.left.depth if root.right.left else 0
        rrd = root.right.right.depth if root.right.right else 0
        if rrd >= rld:
            return leftRotation(root)                                                                                                                                                                                                                                                                               
        else:
            root.right = rightRotation(root.right)
            return leftRotation(root)


'''
BST operations
    1. insert(TreeNode, int) -> TreeNode : Insert an element into AVL tree.
    2. delete(TreeNode, int) -> TreeNode : Delete an element from AVL tree.
    3. traverse(TreeNode) -> List[int] : Inorder traverse, return an ordered sequence.
    4. show(TreeNode) -> None : Show the tree structure.
    5. search(TreeNode, int) -> TreeNode : Search for an element in the tree, return the node if exists, and None if not.
    6. min_(TreeNode, int) -> int : Return the mininum element in tree.
    7. max_(TreeNode, int) -> int : Return the maximum element in tree.
'''
def insert(root: TreeNode, val) -> TreeNode:
    if root == None:
        return TreeNode(val)
    if root.val > val:
        root.left = insert(root.left, val)
        return rebalance(root)
    elif root.val < val:
        root.right = insert(root.right, val)
        return rebalance(root)   
    else:
        return root


def delete(root: TreeNode, val) -> TreeNode:
    if root == None or (not root.right and not root.left):
        return None
    elif root.val != val:
        if root.val > val:
            root.left = delete(root.left, val)
        else:
            root.right = delete(root.right, val)
        return rebalance(root)
    else:
        stack = [root]
        if root.right:
            prev, cur = root, root.right
            while cur.left:
                prev, cur = cur, cur.left
                stack.append(prev)
        else:
            prev, cur = root, root.left
            while cur.right:
                prev, cur = cur, cur.right
                stack.append(prev)
        root.val = cur.val
        if cur.val < prev.val:
            prev.left = delete(cur, cur.val)
        else:
            prev.right = delete(cur, cur.val)
        while len(stack) > 1:
            prev = stack.pop()
            if prev == stack[-1].left:
                stack[-1].left = rebalance(prev)
            else:
                stack[-1].right = rebalance(prev)
        return rebalance(root)


def traverse(root: TreeNode):
    res = []
    if root:
        res.extend(traverse(root.left))
        res.append(root.val)
        res.extend(traverse(root.right))
    return res


def show(root: TreeNode):
    if root:
        # Show the left and right child of each node.
        print('%d->%s, %s' % (root.val, str(root.left.val if root.left else 'None'),
                    str(root.right.val if root.right else 'None')))
        show(root.left)
        show(root.right)


def search(root: TreeNode, val) -> TreeNode:
    if root:
        if root.val > val:
            return search(root.left, val)
        elif root.val < val:
            return search(root.right, val)
        else:
            return root
    return None


def min_(root: TreeNode):
    if root == None:
        return 0xffffffff
    cur = root
    while cur.left:
        cur = cur.left
    return cur.val


def max_(root: TreeNode):
    if root == None:
        return 0x3fffffff
    cur = root
    while cur.right:
        cur = cur.right
    return cur.val


'''
Demo
'''
if __name__ == '__main__':
    root = None
    while True:
        s = input()
        if not s:
            break
        params = s.split()
        op = params[0]
        if op == 'i':   # insert
            root = insert(root, int(params[1]))
        elif op == 'd': # delete
            root = delete(root, int(params[1]))
        elif op == 't': # traverse
            print(traverse(root))
        elif op == 's': # show
            show(root)
        elif op == 'm': # max and min
            print(max_(root), min_(root))
        else:
            print('Unexpected oparator: %s.' % op)