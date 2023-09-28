"""
В данном модуле содержится
класс App
"""


class App:
    """
    Данный класс содержит основные поля, необходимые
    для работы нашего приложения. Также данный класс
    использует паттерн singleton (для удобного
    использования единственного экземпляра
    во всех модулях)
    """
    _instance = None
    is_pause = False
    thread_flag = False
    playlist = None
    play_with_threading = None
    playlists = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance
