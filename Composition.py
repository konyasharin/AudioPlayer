class Composition:
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        if isinstance(other, Composition):
            return self.path == other.path
        return False
