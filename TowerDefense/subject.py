from interface import Interface


class Subject(Interface):
    def register_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observers(self):
        pass
