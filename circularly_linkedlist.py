class node:
    def __init__(self,data):
        self.database
        self.next=None
    
def count_Nodes(tail):
    if not head:
        return 0
    count =0
    current=head

    while True:
        count +=1
        current=current.next
        if current == head:
            break
    return count