class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


root = TreeNode(10)
left_child = TreeNode(5)
right_child = TreeNode(15)

root.left = left_child
root.right = right_child
root.left.left = TreeNode(2)
root.left.right = TreeNode(8)
root.right.left = TreeNode(12)
root.right.right = TreeNode(20)


print("root: ", root.data)
print("left child: ", root.left.data)
print("right child: ", root.right.data)

def print_in_order(node):
    if node is None:
        return
    
    print_in_order(node.left)
    print(node.data, end=" ")
    print_in_order(node.right)

def print_pre_order(node):
    if node is None:
        return
    
    print(node.data, end=" ")
    print_pre_order(node.left)
    print_pre_order(node.right)

def print_post_order(node):
    if node is None:
        return
    
    print_post_order(node.left)
    print_post_order(node.right)
    print(node.data, end=" ")


print("\ninorder:")
print_in_order(root)
print()

print("\npreorder:")
print_pre_order(root)
print()

print("\npostorder:")
print_post_order(root)
print()