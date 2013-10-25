class Tally:
    def __init__(self):
        self.array = []
    def expand_to_index(self, index):
        while len(self.array) <= index:
            self.array.append(0)
    def get(self, index):
        if index < 0:
            return 0
        self.expand_to_index(index)
        return self.array[index]
    def set(self, index, value):
        self.expand_to_index(index)
        self.array[index] = value
    def inc(self, index, delta):
        self.expand_to_index(index)
        self.array[index] = self.array[index] + delta
    def dec(self, index, delta):
        self.expand_to_index(index)
        self.array[index] = self.array[index] - delta
        
        
        