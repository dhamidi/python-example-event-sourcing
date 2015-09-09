from nose.tools import *
from es_example import *
import os
import tempfile


TEST_DB_NAME='test-events.db'

class ReplayedEvents:
    def __init__(self):
        self.events = []

    def handle_event(self, event):
        self.events.append(event)
        return self


def do_nothing():
    pass

def delete_persistent():
    os.remove(TEST_DB_NAME)

@with_setup(do_nothing,delete_persistent)
def test_stored_events_can_be_replayed():
    store = EventsOnDisk(TEST_DB_NAME)
    event = Event('user.signed-up', {
        'aggregate_id': 'the-user',
        'username': 'the-user',
    })
    replayed = ReplayedEvents()
    store.store([event])
    store.replay_all(replayed)

    assert_in(event, replayed.events)

@with_setup(do_nothing, delete_persistent)
def test_stored_events_can_be_replayed_by_aggregate_id():
    store = EventsOnDisk(TEST_DB_NAME)
    event_for_first_user = Event('user.signed-up', {
        'aggregate_id': 'the-user',
        'username': 'the-user',
    })
    event_for_second_user = Event('user.signed-up', {
        'aggregate_id': 'the-other-user',
        'username': 'the-other-user',
    })
    replayed = ReplayedEvents()
    store.store([event_for_first_user, event_for_second_user])
    store.replay_for_aggregate('the-other-user', replayed)

    assert_not_in(event_for_first_user, replayed.events)
    assert_in(event_for_second_user, replayed.events)
