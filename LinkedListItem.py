"""
Данный модуль содержит класс LinkedListItem
(элемент LinkedList)
"""


class LinkedListItem:
    """
    Данный класс содержит:
    prev - ссылка на предыдущий элемент списка
    next - ссылка на следующий элемент списка
    track - данный элемент списка
    метод __eq__ для сравнения двух LinkedListItem
    """
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
        """
        Геттер _next
        :return: _next
        """
        return self._next

    @next.setter
    def next(self, item):
        self._next = item

    @property
    def prev(self):
        """
        Геттер _prev
        :return: _prev
        """
        return self._prev

    @prev.setter
    def prev(self, item):
        self._prev = item
