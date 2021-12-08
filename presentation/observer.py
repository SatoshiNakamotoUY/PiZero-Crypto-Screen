class Observer:
    def __init__(self, observable):
        observable.register(self)

    def update(self, coin, data):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def update_observers(self, coin, data):
        for observer in self._observers:
            observer.update(coin, data)

    def close(self):
        for observer in self._observers:
            observer.close()
