class HashTable(object):
    def __init__(self, size):
        self.__count = 0
        self.__table = [None] * size

    def hash(self, key):
        hashed = 0
        for char in str(key):
            hashed += ord(char)
        return hashed % len(self.__table)

    def add(self, key, item):
        hashed = self.hash(key)
        pair = [key, item]
        will_append = True

        if self.__table[hashed] is None:
            self.__table[hashed] = list()

        for inhabitant in self.__table[hashed]:
            will_append = inhabitant[0] != key
            if not will_append:
                inhabitant[1] = pair[1]
                break

        if will_append:
            self.__table[hashed].append(pair)
            self.__count = self.__count + 1

    def get(self, key):
        hashed = self.hash(key)
        pairs = self.__table[hashed]

        if pairs is None:
            return pairs
        try:
            return next((pair[1] for pair in pairs if pair[0] == key))
        except:
            return None

    def delete(self, key):
        hashed = self.hash(key)
        pairs = self.__table[hashed]

        if pairs is None:
            return pairs

        for pair in pairs: 
            if pair[0] == key:
                pairs.remove(pair)
        pass

    def get_count(self):
        return self.__count
