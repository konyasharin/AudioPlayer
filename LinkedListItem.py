class LinkedListItem:
    def __init__(self, item):
        self.track = item
        self._next = None
        self._prev = None

    def __eq__(self, other):
        if isinstance(other, LinkedListItem):
            return self.track == other.track
        return False

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, item):
        self._next = item

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, item):
        self._prev = item
