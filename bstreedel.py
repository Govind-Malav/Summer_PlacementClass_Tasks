class DatabaseNode:
    def __init__(self,user_id,user_data):
        self.id=user_id
        self.user_data=user_data
        self.left=None
        self.right=None
        
def find_min_value_node(root,target_id):
    current=node
    while current.left is not None:
        current=current.left
    return current
    
def delete_user(root,target_id):
    if root is None:
        return root

    if target_id<root.id:
        root.left=delete_user(root.left,target_id)
    elif target_id>root.id:
        root.right=delete_user(root.right,target_id)

    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        
        succesor=find_min_value_node(root.right)

        root.id=succesor.id
        root.data=succesor.data

        root.right=delete_user(root.right,succesor.id)

    return root

def validate_bst_helper(node,min_val=-float('inf'),max_val=float('inf')):
    if node is None:
        return True

    if not (min_val<node.id<max_val):
        return False

    return (validate_bst_helper(node.left,min_val,node.id) and validate_bst_helper(node.right,node.id,max_val))

def is_valid(root):
    return validate_bst_helper(root)


good_tree=DatabaseNode(50,"userA")
good_tree.left=DatabaseNode(30,"userB")
good_tree.right=DatabaseNode(70,"userC")


print(f"is this database index corrupted? {'NO' if is_valid(good_tree) else 'YES'}")

bad_tree=DatabaseNode(50,"userA")
bad_tree.left=DatabaseNode(70,"userB")
bad_tree.right=DatabaseNode(30,"userC")

print(f"is this database index corrupted? {'NO' if is_valid(bad_tree) else 'YES'}")