import weakref

class EventPublisher:
    """Миксин для классов, генерирующих события. Хранит подписчиков через слабые ссылки."""
    def __init__(self):
        self._listeners = {}   # event_type -> list of weakrefs to bound methods

    def subscribe(self, event_type, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        # Создаём слабую ссылку на метод
        wr = weakref.WeakMethod(callback)
        # Проверяем, нет ли уже такой же (по объекту и имени метода)
        for existing in self._listeners[event_type]:
            if existing() == callback:
                return
        self._listeners[event_type].append(wr)

    def unsubscribe(self, event_type, callback):
        if event_type in self._listeners:
            self._listeners[event_type] = [
                wr for wr in self._listeners[event_type]
                if wr() != callback
            ]
            if not self._listeners[event_type]:
                del self._listeners[event_type]

    def unsubscribe_all_for_callback(self, callback):
        """Удаляет все слабые ссылки на данный метод."""
        for event_type in list(self._listeners.keys()):
            self._listeners[event_type] = [
                wr for wr in self._listeners[event_type]
                if wr() != callback
            ]
            if not self._listeners[event_type]:
                del self._listeners[event_type]

    def notify(self, event_type, **data):
        if event_type not in self._listeners:
            return
        alive = []
        for wr in self._listeners[event_type]:
            callback = wr()
            if callback is not None:
                try:
                    callback(event_type, data)
                except Exception as e:
                    print(f"[Event] Ошибка в обработчике {event_type}: {e}")
                    import traceback
                    traceback.print_exc()
                alive.append(wr)
            # если callback is None – ссылка умерла, не добавляем
        if alive:
            self._listeners[event_type] = alive
        else:
            del self._listeners[event_type]