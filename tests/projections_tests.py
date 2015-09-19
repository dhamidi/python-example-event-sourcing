from nose.tools import *
from es_example import Event
import es_example.projection as projection

def test_AllUsersProjection_adds_user_on_sign_up():
    all_users = projection.AllUsers()
    event = Event('user.signed-up', {
        'username': 'the-user',
        'aggregate_id': 'the-user',
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'secret',
    })

    all_users.handle_event(event)
    user = all_users.find('the-user')
    assert_equal(user.username, 'the-user')
    assert_equal(user.name, 'John Doe')
    assert_equal(user.email, 'john.doe@example.com')

def test_AllUsersProjection_lists_all_users():
    all_users = projection.AllUsers()
    events = [
        Event('user.signed-up', {
            'username': 'the-user',
            'aggregate_id': 'the-user',
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'secret',
        }),
        Event('user.signed-up', {
            'username': 'the-other-user',
            'aggregate_id': 'the-other-user',
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'password': 'secret',
        }),
    ]

    for event in events:
        all_users.handle_event(event)

    result = all_users.index()
    assert_equal(
        [x.username for x in result],
        ['the-user', 'the-other-user'],
    )
