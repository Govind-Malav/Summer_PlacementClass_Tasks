class Node:
    def __init__(self, name, cut=None):
        self.name = name
        self.cut = cut
        self.left = None
        self.right = None
        self.width = 0
        self.height = 0


class SlicingFloorPlan:
    def __init__(self):
        self.root = None

    def create_rectangle(self, name, width, height):
        self.root = Node(name)
        self.root.width = width
        self.root.height = height

    def horizontal_cut(self, node, left_name, right_name, w1, h1, w2, h2):
        node.cut = "H"
        node.left = Node(left_name)
        node.right = Node(right_name)
        node.left.width = w1
        node.left.height = h1
        node.right.width = w2
        node.right.height = h2

    def vertical_cut(self, node, left_name, right_name, w1, h1, w2, h2):
        node.cut = "V"
        node.left = Node(left_name)
        node.right = Node(right_name)
        node.left.width = w1
        node.left.height = h1
        node.right.width = w2
        node.right.height = h2

    def compact(self, node):
        if node.left is None and node.right is None:
            return node.width, node.height

        lw, lh = self.compact(node.left)
        rw, rh = self.compact(node.right)

        if node.cut == "H":
            node.width = max(lw, rw)
            node.height = lh + rh
        else:
            node.width = lw + rw
            node.height = max(lh, rh)

        return node.width, node.height

    def display(self, node):
        if node is None:
            return
        print(node.name, node.cut, node.width, node.height)
        self.display(node.left)
        self.display(node.right)


plan = SlicingFloorPlan()

plan.create_rectangle("A", 10, 8)

plan.horizontal_cut(plan.root, "B", "C", 5, 4, 6, 3)

plan.vertical_cut(plan.root.left, "D", "E", 2, 4, 3, 4)

plan.compact(plan.root)

print("Slicing Tree")
plan.display(plan.root)

print("Minimum Width :", plan.root.width)
print("Minimum Height:", plan.root.height)