"""Тесты модуля linked_list"""

import unittest

from LinkedListItem import LinkedListItem  
from LinkedList import LinkedList  # pylint: disable=E0401

TEST_LEN = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]

TEST_LAST = TEST_LEN

TEST_REMOVE = [
    ([1], 1),
    ([1, 1, 1], 1),
    ([2, 1, 1, 3], 1),
    ([2, 3, 4], 2),
    ([2, 3, 4], 4),
]

TEST_REMOVE_FAILED = [
    ([], 1),
    ([1], 2),
    ([1, 1, 1, 3, 4], 2),
]

TEST_CONTAINS = [
    ([], 1, False),
    ([1], 1, True),
    ([1], 2, False),
    ([1, 1, 1], 1, True),
    ([2, 3], 5, False),
    ([2, 3], 3, True),
]

TEST_GETITEM = [
    ([2], 0),
    ([4], -1),
    ([5, 1], 1),
    ([5, 1], -2),
    ([2, 0, 1, 4, 2], 2),
]

TEST_GETITEM_FAILED = [
    ([], 0),
    ([1], 1),
    ([1], -2),
    ([1, 2, 3], 3),
    ([1, 2, 4], -4),
]

TEST_INSERT = [
    # (create_linked_list([]), 0, 42),
    ([1], 0, 42),
    # (create_linked_list([2]), 1, 42),
    ([1, 2, 3], 1, 42),
    ([1, 2, 3], 0, 42),
]


def create_linked_list(nodes_list):
    """Создание связного списка"""
    linked_list = LinkedList()
    for item in nodes_list:
        node = LinkedListItem(item)
        linked_list.append(node)
    return linked_list


class TestLinkedListItem(unittest.TestCase):
    """Тест-кейс класса LinkedListItem"""
    def test_next_item(self):
        """Тест соединения узлов через next_item"""
        node_a = LinkedListItem(42)
        node_b = LinkedListItem(196)
        node_a.next = node_b
        node_b.prev = node_a
        self.assertTrue(node_a.next is node_b)
        self.assertTrue(node_a.prev is None)
        self.assertTrue(node_b.next is None)
        self.assertTrue(node_b.prev is node_a)

    def test_previous_item(self):
        """Тест соединения узлов через previous_item"""
        node_a = LinkedListItem(42)
        node_b = LinkedListItem(196)
        node_b.prev = node_a
        node_a.next = node_b
        self.assertTrue(node_a.next is node_b)
        self.assertTrue(node_a.prev is None)
        self.assertTrue(node_b.next is None)
        self.assertTrue(node_b.prev is node_a)


class TestLinkedList(unittest.TestCase):
    """Тест-кейс класса LinkedList"""
    def test_len(self):
        """Тест метода len"""
        i = 0
        linked_list = LinkedList()
        for expected_len in TEST_LEN:
            i += 1
            node = LinkedListItem(expected_len)
            linked_list.append(node)
            with self.subTest(expected_len=expected_len):
                self.assertEqual(len(linked_list), i)

    def test_last(self):
        """Тест свойства last"""
        for expected_len in TEST_LAST:
            last = None
            linked_list = LinkedList()
            for i in range(expected_len):
                node = LinkedListItem(i)
                linked_list.append(node)
                last = node
            with self.subTest(expected_len=expected_len):
                self.assertEqual(linked_list.last(), last)

    def test_append_left(self):
        """Тест метода append_left"""
        for expected_len in TEST_LAST:
            first = None
            linked_list = LinkedList()
            for i in range(expected_len):
                node = LinkedListItem(i)
                if i == expected_len - 1:
                    first = node
                linked_list.append_left(node)
            with self.subTest(expected_len=expected_len):
                self.assertEqual(linked_list[0], first)

    def test_append_right(self):
        """Тест метода append_right"""
        for expected_len in TEST_LAST:
            last = None
            linked_list = LinkedList()
            for i in range(expected_len):
                node = LinkedListItem(i)
                if i == expected_len - 1:
                    last = node
                linked_list.append_right(node)
            with self.subTest(expected_len=expected_len):
                self.assertEqual(linked_list.last(), last)

    def test_append(self):
        """Тест метода append"""
        for expected_len in TEST_LAST:
            last = None
            linked_list = LinkedList()
            for i in range(expected_len):
                node = LinkedListItem(i)
                if i == expected_len - 1:
                    last = node
                linked_list.append(node)
            with self.subTest(expected_len=expected_len):
                self.assertEqual(linked_list.last(), last)

    def test_remove(self):
        """Тест метода remove"""
        for node_list, remove_item in TEST_REMOVE:
            linked_list = create_linked_list(node_list)
            with self.subTest(node_list=node_list, remove_item=remove_item):
                linked_list.remove(LinkedListItem(remove_item))
                self.assertEqual(len(linked_list), len(node_list) - 1)

    def test_remove_failed(self):
        """Тест метода remove с исключением ValueError"""
        for node_list, remove_item in TEST_REMOVE_FAILED:
            linked_list = create_linked_list(node_list)
            with self.subTest(node_list=node_list, remove_item=remove_item):
                linked_list.remove(remove_item)
                self.assertEqual(len(linked_list), len(node_list))

    def test_insert(self):
        """Тест метода insert"""
        for node_list, index, data in TEST_INSERT:
            linked_list = create_linked_list(node_list)
            with self.subTest(node_list=node_list, index=index,
                              data=data):
                linked_list.insert(index, LinkedListItem(data))
                self.assertEqual(len(linked_list), len(node_list) + 1)
                node_list.insert(index + 1, data)
                self.assertEqual([i.track for i in linked_list], node_list)

    def test_getitem(self):
        """Тест индексации"""
        for node_list, index in TEST_GETITEM:
            linked_list = create_linked_list(node_list)
            with self.subTest(node_list=node_list, index=index):
                item = linked_list[index]
                self.assertEqual(item.track, node_list[index])

    def test_getitem_failed(self):
        """Тест индексации с исключением IndexError"""
        for node_list, index in TEST_GETITEM_FAILED:
            linked_list = create_linked_list(node_list)
            with self.subTest(node_list=node_list, index=index):
                item = linked_list[index]
                self.assertEqual(item, None)

    def test_contains(self):
        """Тест поддержки оператора in"""
        for node_list, item, expected in TEST_CONTAINS:
            linked_list = create_linked_list(node_list)
            with self.subTest(node_list=node_list, item=item, expected=expected):
                self.assertTrue((LinkedListItem(item) in linked_list) is expected)

    def test_reversed(self):
        """Тест поддержки функции reversed"""
        for i in TEST_LEN:
            linked_list = create_linked_list(list(range(i)))
            with self.subTest(node_list=list(range(i))):
                self.assertEqual(
                    [item.track for item in reversed(linked_list)],
                    list(range(i - 1, -1, -1))
                )
