class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift
    def encrypt(self, text):
        result = ""
        for ch in text:
            if ch.isupper():
                value = ord(ch) - ord('A')
                value = (value + self.shift) % 26
                result = result + chr(value + ord('A'))
            elif ch.islower():
                value = ord(ch) - ord('a')
                value = (value + self.shift) % 26
                result = result + chr(value + ord('a'))
            else:
                result = result + ch
        return result
    def decrypt(self, text):
        result = ""
        for ch in text:
            if ch.isupper():
                value = ord(ch) - ord('A')
                value = (value - self.shift) % 26
                result = result + chr(value + ord('A'))
            elif ch.islower():
                value = ord(ch) - ord('a')
                value = (value - self.shift) % 26
                result = result + chr(value + ord('a'))
            else:
                result = result + ch
        return result