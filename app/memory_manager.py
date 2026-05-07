class MemoryManager:
    def __init__(self):
        self.memory = {}

    def __setitem__(self, key, value):
        self.memory[key] = value
    def __contains__(self, key):
        return key in self.memory
    def __delitem__(self, key):
        del self.memory[key]
    def __getitem__(self, item):
        if item in self.memory:
            return self.memory[item]
        return None
    def get(self, key, default=None):
        if key in self.memory:
            return self.memory[key]
        return default
