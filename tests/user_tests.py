from nose.tools import *
from es_example import *

@raises(ValidationError)
def test_User_sign_up_raises_error_if_user_signed_up_already():
    events = EventsInMemory()
    user = User('the-user', events)

    user.handle_event(Event('user.signed-up', {
        'aggregate_id': 'the-user',
        'username': 'the-user',
        'password': 'secret',
        'email': 'foo@example.com',
    }))

    user.handle_command(SignUp(username='the-user',
                               password='secret',
                               email='foo@example.com',
    ))

def test_User_sign_up_publishes_an_event():
    events = EventsInMemory()
    user = User('the-user', events)
    user.handle_command(SignUp(username='the-user',
                               password='secret',
                               email='foo@example.com',
    ))

    assert_in(Event('user.signed-up', {
        'aggregate_id': 'the-user',
        'username': 'the-user',
        'password': 'secret',
        'email': 'foo@example.com',
    }), events.published())
