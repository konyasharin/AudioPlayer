"""
Данный модуль хранит в себе класс Composition
"""


class Composition:
    """
    Данный класс содержит в себе метод __eq__ для
    сравнения двух экземпляров на равенство, а также
    path - путь до композиции на ПК
    """
    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        if isinstance(other, Composition):
            return self.path == other.path
        return False
