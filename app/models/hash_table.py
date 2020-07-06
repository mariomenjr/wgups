class HashTable(object):
    def __init__(self, size):
        self.__table = [None] * size

    def hash(self, key):
        hashed = 0
        for char in str(key):
            hashed += ord(char)
        return hashed % len(self.__table)
    
    def add(self, key, item):
        hashed = self.hash(key)
        pair = [key, item]

        if self.__table[hashed] is None:
            self.__table[hashed] = list([pair])
        else:
            for inhabitant in self.__table[hashed]:
                if inhabitant[0] == key:
                    inhabitant[1] = pair[1]
            self.__table[hashed].append(pair)

    def get(self, key):
        hashed = self.hash(key)
        pairs = self.__table[hashed]
        
        if pairs is None:
            return pairs
        
        return next((pair[1] for pair in pairs if pair[0] == key))