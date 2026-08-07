class EventPublisher:
    """Миксин для классов, которые могут генерировать события."""
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(callback)
            except ValueError:
                pass

    def unsubscribe_all_for_callback(self, callback):
        for event_type in list(self._listeners.keys()):
            try:
                self._listeners[event_type].remove(callback)
            except ValueError:
                pass
            if not self._listeners[event_type]:
                del self._listeners[event_type]

    def notify(self, event_type, **data):
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(event_type, data)
                except Exception as e:
                    print(f"[Event] Ошибка в обработчике {event_type}: {e}")
                    import traceback
                    traceback.print_exc()