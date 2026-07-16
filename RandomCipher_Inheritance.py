import random
class SubstitutionCipher:
    def __init__(self, key):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.forward = {}
        self.backward = {}
        for i in range(26):
            self.forward[letters[i]] = key[i]
            self.backward[key[i]] = letters[i]
    def encrypt(self, text):
        result = ""
        for ch in text:
            if ch.isupper():
                result = result + self.forward[ch]
            elif ch.islower():
                result = result + self.forward[ch.upper()].lower()
            else:
                result = result + ch
        return result
    def decrypt(self, text):
        result = ""
        for ch in text:
            if ch.isupper():
                result = result + self.backward[ch]
            elif ch.islower():
                result = result + self.backward[ch.upper()].lower()
            else:
                result = result + ch
        return result
class RandomCipher(SubstitutionCipher):
    def __init__(self):
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(letters)
        key = ""
        for ch in letters:
            key = key + ch
        super().__init__(key)
        print("Random Key :", key)
