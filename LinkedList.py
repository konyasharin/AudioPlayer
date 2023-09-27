"""
Данный модуль содержит класс LinkedList
(Кольцевой двусвязный список)
"""


class LinkedList:
    """
    Данный класс содержит в себе все операции для работы с
    кольцевыми двусвязными списками
    """
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.current = None

    def append_right(self, item):
        """
        Данный метод добавлет item в конец списка
        :param item: LinkedListItem, который мы вставляем
        """
        if self.start_node is None:
            self.start_node = item
        elif self.end_node is None:
            self.end_node = item
            self.end_node.prev = self.start_node
            self.end_node.next = self.start_node
            self.start_node.next = self.end_node
            self.start_node.prev = self.end_node
        else:
            item.prev = self.end_node
            item.next = self.start_node
            self.end_node = item
            self.end_node.prev.next = self.end_node
            self.start_node.prev = self.end_node

    def append(self, item):
        """
        Данный метод работает как метод append_right
        :param item: LinkedListItem, который мы вставляем
        """
        self.append_right(item)

    def append_left(self, item):
        """
        Данный метод добавлет item в начало списка
        :param item: LinkedListItem, который мы вставляем
        """
        if self.start_node is None:
            self.start_node = item
        elif self.end_node is None:
            self.end_node = self.start_node
            self.start_node = item
            self.start_node.next = self.end_node
            self.start_node.prev = self.end_node
            self.end_node.prev = self.start_node
            self.end_node.next = self.start_node
        else:
            item.next = self.start_node
            item.prev = self.end_node
            self.start_node = item
            self.start_node.next.prev = self.start_node
            self.end_node.next = self.start_node

    def remove(self, item):
        """
        Данный метод удаляет первый попавшийся в списке item
        :param item: LinkedListItem, который мы удаляем
        """
        for elem in self:
            check_elem = elem
            if check_elem == item:
                if check_elem == self[0]:
                    if len(self) == 1:
                        self.start_node = None
                    else:
                        self.start_node = check_elem.next
                elif check_elem == self[len(self) - 1]:
                    if len(self) == 1:
                        self.end_node = None
                    else:
                        self.end_node = check_elem.prev
                if check_elem.prev is not None:
                    check_elem.prev.next = check_elem.next
                if check_elem.next is not None:
                    check_elem.next.prev = check_elem.prev
                print("Элемент успешно удален")
                return
    print("Данного элемента не существует")

    def insert(self, previous_index, item):
        """
        Данный метод добавлет item после LinkedList[previous_index]
        :param item: LinkedListItem, который мы вставляем
        :param previous_index: индекс элемента, после которого
        мы вставляем item
        """
        check_elem = self[previous_index]
        if len(self) == 1 and previous_index == 0:
            self.append(item)
        check_elem.next.prev = item
        item.next = check_elem.next
        item.prev = check_elem
        check_elem.next = item
        if check_elem == self[len(self) - 1]:
            self.end_node = item
        print("Элемент успешно добавлен")

    def _check_none(self):
        """
        Данный метод получает первый элемент в списке
        (Первым может оказаться и end_node, если start_node is None)
        :return: первый элемент в списке
        """
        if self.start_node is not None and self.end_node is None:
            check_elem = self.start_node
        elif self.start_node is None and self.end_node is not None:
            check_elem = self.end_node
        elif self.start_node is None and self.end_node is None:
            return None
        else:
            check_elem = self.start_node
        return check_elem

    def last(self):
        """
        Данный метод получает последний элемент списка
        :return: последний элемент в списке
        """
        if len(self) >= 2:
            return self.end_node
        if len(self) == 1:
            return self.start_node
        return None

    def __iter__(self):
        self.current = 0
        return self

    def __len__(self):
        count = 0
        node = self._check_none()
        while node:
            count += 1
            if node == self.start_node and self.end_node is None:
                break
            node = node.next
            if (node == self.end_node and self.start_node is not None
                    and self.end_node is not None):
                count += 1
                break
        return count

    def __next__(self):
        if self.current < len(self):
            self.current += 1
            return self[self.current - 1]
        raise StopIteration

    def __getitem__(self, index):
        i = 0
        check_elem = self._check_none()
        if index >= len(self) or index < -len(self):
            print("Вы используете недопустимый индекс!")
            return None
        if check_elem is None:
            return None
        if index >= 0:
            while i != index:
                check_elem = check_elem.next
                i += 1
        else:
            check_elem = self.last()
            i = -1
            while i != index:
                check_elem = check_elem.prev
                i -= 1
        return check_elem

    def __contains__(self, item):
        for elem in self:
            if elem == item:
                return True
        return False

    def __reversed__(self):
        for i in range(-1, -len(self) - 1, -1):
            yield self[i]
