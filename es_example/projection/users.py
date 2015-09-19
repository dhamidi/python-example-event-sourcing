from collections import namedtuple
import shelve

User = namedtuple('User', ['username', 'email', 'name'])

class AllUsers:
    event_handlers = {
        'user.signed-up': '_on_user_signed_up'
    }

    def __init__(self):
        self._byId = {}
        self._index = []

    def load(self, filename):
        with shelve.open(filename) as db:
            try:
                self._byId = db['_byId']
                self._index = db['_index']
            except KeyError:
                pass

    def persist(self, filename):
        with shelve.open(filename) as db:
            db['_byId'] = self._byId
            db['_index'] = self._index

    def index(self):
        return self._index

    def find(self, aggregate_id):
        return self._byId[aggregate_id]

    def handle_event(self, event):
        try:
            getattr(self, self.event_handlers[event.name()])(event)
        except KeyError:
            pass

    def _on_user_signed_up(self, event):
        params = {key: event.payload().get(key) for key in User._fields}
        user = User(**params)
        self._byId[event.aggregate_id()] = user
        self._index.append(user)
