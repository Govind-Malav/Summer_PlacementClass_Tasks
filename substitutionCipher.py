class SubstitutionCipher:
    def __init__(self, key):
        self.upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.forward = {}
        self.backward = {}
        for i in range(26):
            self.forward[self.upper[i]] = key[i]
            self.backward[key[i]] = self.upper[i]
    def encrypt(self, text):
        result = ""
        for ch in text:
            if ch.isupper():
                result = result + self.forward[ch]
            elif ch.islower():
                upper = ch.upper()
                result = result + self.forward[upper].lower()
            else:
                result = result + ch
        return result
    def decrypt(self, text):
        result = ""
        for ch in text:
            if ch.isupper():
                result = result + self.backward[ch]
            elif ch.islower():
                upper = ch.upper()
                result = result + self.backward[upper].lower()
            else:
                result = result + ch
        return result