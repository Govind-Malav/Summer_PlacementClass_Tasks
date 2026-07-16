from collections import deque
class NetworkNode:
    def __init__(self, username):
        self.username = username
        self.left = None
        self.right = None

def level_order_by_layers(root):
    if root is None:
        return []

    layers = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level_node = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level_node.append(node.username)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        layers.append(current_level_node)
    return layers

company = NetworkNode("ceo")
company.left = NetworkNode("vp_engineering")
company.right = NetworkNode("vp_sales")

company.left.left = NetworkNode("eng_lead1")
company.left.right = NetworkNode("eng_lead2")

print(level_order_by_layers(company))