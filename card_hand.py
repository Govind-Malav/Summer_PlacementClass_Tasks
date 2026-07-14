class Node:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.prev = None
        self.next = None


class CardHand:
    def __init__(self):
        self.head = None
        self.tail = None
        self.fingers = {
            "Hearts": None,
            "Clubs": None,
            "Spades": None,
            "Diamonds": None
        }

    def add_card(self, rank, suit):
        new = Node(rank, suit)
        if self.head is None:
            self.head = self.tail = new
            self.fingers[suit] = new
            return
        if self.fingers[suit]:
            last = self.fingers[suit]

            new.next = last.next
            new.prev = last

            if last.next:
                last.next.prev = new
            else:
                self.tail = new

            last.next = new
            self.fingers[suit] = new

        else:
            self.tail.next = new
            new.prev = self.tail
            self.tail = new
            self.fingers[suit] = new

    def play(self, suit):
        current = self.head
        while current:
            if current.suit == suit:
                self.remove(current)
                return (current.rank, current.suit)
            current = current.next
        if self.head:
            temp = self.head
            self.remove(temp)
            return (temp.rank, temp.suit)

        return None

    def remove(self, node):
        if self.fingers[node.suit] == node:
            temp = node.prev
            while temp and temp.suit != node.suit:
                temp = temp.prev
            self.fingers[node.suit] = temp

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def __iter__(self):
        current = self.head
        while current:
            yield (current.rank, current.suit)
            current = current.next

    def all_of_suit(self, suit):
        current = self.head
        while current:
            if current.suit == suit:
                yield current.rank
            current = current.next


hand = CardHand()

hand.add_card("A", "Hearts")
hand.add_card("10", "Spades")
hand.add_card("K", "Hearts")
hand.add_card("7", "Clubs")
hand.add_card("5", "Diamonds")

print("Cards in hand:")
for card in hand:
    print(card)

print("\nPlayed:", hand.play("Hearts"))

print("\nRemaining cards:")
for card in hand:
    print(card)

print("\nSpades:")
for card in hand.all_of_suit("Spades"):
    print(card)