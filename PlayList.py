from LinkedList import LinkedList


class PlayList(LinkedList):
    def __init__(self):
        super().__init__()
        self.current_track = None
