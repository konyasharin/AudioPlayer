class AudioPlayer:
    instance = None  # Использование паттерна Singleton(у нас единственный экземпляр данного класса на всю программу)

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(AudioPlayer, cls).__new__(cls)
        return cls.instance
