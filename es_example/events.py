import shelve

class Event:
    def __init__(self, name, payload):
        self._name = name
        self._aggregate_id = payload['aggregate_id']
        self._payload = payload

    def __repr__(self):
        return "<Event %s %s>" % (self.name(), self.payload())

    def __eq__(self, other):
        return self.name() == other.name() and self.payload() == other.payload()

    def name(self):
        return self._name

    def aggregate_id(self):
        return self._aggregate_id

    def payload(self):
        return self._payload

class EventsInMemory:
    def __init__(self):
        self._published = []

    def publish(self, event):
        self._published.append(event)
        return self

    def replay_all(self, handler):
        for event in self._published:
            handler.handle_event(event)

    def replay_for_aggregate(self, aggregate_id, handler):
        for event in self._published:
            if event.aggregate_id() == aggregate_id:
                handler.handle_event(event)

    def store(self, events):
        self._published.extend(events)

    def published(self):
        return self._published

class EventsOnDisk:
    def __init__(self, filename):
        self.filename = filename

    def store(self,events):
        with shelve.open(self.filename) as db:
            try:
                sequence_number = db['sequence_number']
            except KeyError:
                sequence_number = 0

            append_to_index = []
            for event in events:
                sequence_number = sequence_number + 1
                event_id = 'event_%d' % sequence_number
                db[event_id] = event
                append_to_index.append(event_id)

                aggregate_index_key = 'index:%s' % event.aggregate_id()
                try:
                    aggregate_index = db[aggregate_index_key]
                except KeyError:
                    aggregate_index = []

                aggregate_index.append(event_id)
                db[aggregate_index_key] = aggregate_index

            try:
                index = db['index']
            except KeyError:
                index = []

            index.extend(append_to_index)
            db['index'] = index

    def replay_all(self, handler):
        with shelve.open(self.filename) as db:
            try:
                index = db['index']
            except KeyError:
                index = []

            for event_id in index:
                event = db[event_id]
                handler.handle_event(event)

    def replay_for_aggregate(self, aggregate_id, handler):
        index_name = 'index:%s' % aggregate_id
        with shelve.open(self.filename) as db:
            try:
                index = db[index_name]
            except KeyError:
                index = []

            for event_id in index:
                event = db[event_id]
                handler.handle_event(event)
