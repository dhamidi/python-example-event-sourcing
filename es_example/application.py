from .events import EventsInMemory
from .errors import ValidationError

class Application:
    def __init__(self,event_store):
        self.event_store = event_store
        self.handlers = []

    def add_event_handler(self, handler):
        self.handlers.append(handler)

    def handle_command(self, command):
        transaction = EventsInMemory()
        aggregate_id = command.aggregate_id()
        aggregate = command.Aggregate(aggregate_id, transaction)
        try:
            self.event_store.replay_for_aggregate(aggregate_id, aggregate)
            aggregate.handle_command(command)
            self.event_store.store(transaction.published())
            for handler in self.handlers:
                transaction.replay_all(handler)
        except ValidationError as e:
            return e

        return True
