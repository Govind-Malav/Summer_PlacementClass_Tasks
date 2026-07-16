class FileNode:
    def __init__(self,name,size_kb):
        self.name=name
        self.size_kb=size_kb
        self.left=None
        self.right=None

def calculate_total_space(root):
    if root is None:
        return 0
    left_space=calculate_total_space(root.left)
    right_space=calculate_total_space(root.right)

    return left_space+right_space +root.size
def find_max_depth(root):
    if root is None:
        return 0
    left_depth=find_max_depth(root.left)
    right_depth=find_max_depth(root.right)

    return max(left_depth,right_depth)+1

def count_leaf_files(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    
    return  count_leaf_files(root.left)+count_leaf_files(root.right)

drive=FileNode("root_drive",50)
drive.left=FileNode("document",20)
drive.right=FileNode("photo",30)
drive.left.left=FileNode("resume",5)
drive.left.right=FileNode("report",10)
drive.right.left=FileNode("pic1",15)
drive.right.right=FileNode("pic2",25)

print(f"Total leaf files:{count_leaf_files(drive)}")