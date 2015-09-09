from nose.tools import *
from es_example import *

class RecordingEventHandler:
    def __init__(self):
        self.events = []
        pass

    def handle_event(self, event):
        self.events.append(event)

def test_Application_calls_event_handlers():
    events = EventsInMemory()
    app = Application(events)
    handler = RecordingEventHandler()
    app.add_event_handler(handler)
    command = SignUp(
        username='the-user',
        email='foo@example.com',
        name='John Doe',
        password='secret',
    )
    app.handle_command(command)

    assert_equal(len(handler.events), 1)

def test_Application_returns_validation_error_if_command_cannot_be_handled():
    events = EventsInMemory()
    app = Application(events)
    handler = RecordingEventHandler()
    app.add_event_handler(handler)
    command = SignUp(
        username='the-user',
        email='foo@example.com',
        name='John Doe',
        password='secret',
    )
    result = app.handle_command(command)
    assert_equal(result, True)
    result = app.handle_command(command)
    assert_is_instance(result, ValidationError)
