def card_shuffle(cards):
    half= len(cards)
    first_half=cards[:half]
    second_half=cards[half:]
    shuffled=[]
    for i in range(half):
        shuffled.append(first_half[i])
        shuffled.append(second_half[i])
    return shuffled

n=int(input("Enter the number of cardcs: "))
cards=[]
print("Enter", 2* n,"elements:")
for i in range(2*n):
    cards.append(int(input()))
result=card_shuffle(cards)
print("Shuffled cards:")
print(result)