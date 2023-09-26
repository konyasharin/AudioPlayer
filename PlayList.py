"""
Данный модуль содержит класс PlayList
"""
from LinkedList import LinkedList


class PlayList(LinkedList):
    """
    Данный класс наследуется от класса LinkedList
    и хранит также в себе текущий трек
    """
    def __init__(self):
        super().__init__()
        self.current_track = None
