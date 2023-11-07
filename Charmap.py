class Charmap:
    def __init__(self, charmap):
        self.ByteToChar = {}
        self.CharToByte = {}
        
        for char, byte in charmap.items():
            if char not in self.CharToByte:
                self.CharToByte[char] = []
            
            if byte not in self.ByteToChar:
                self.ByteToChar[byte] = []
                
            self.ByteToChar[byte].append(char)
            self.CharToByte[char].append(byte)

    def toChar(self, bytes):
        if type(bytes) != list:
            bytes = [bytes]

        return "".join([self.ByteToChar[byte][0] for byte in bytes])
    
    def toBytes(self, chars):
        if type(chars) != list:
            chars = [chars]
            
        return [self.CharToByte[char][0] for char in chars]
