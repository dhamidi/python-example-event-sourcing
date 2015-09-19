from collections import namedtuple
from .errors import ValidationError
from .events import Event

class User:
    event_handlers = {
        'user.signed-up': '_on_signed_up'
    }

    command_handlers = {
        'sign-up': 'sign_up'
    }

    def __init__(self, id, events):
        self.id = id
        self.events = events
        self._signed_up = False

    def handle_event(self, event):
        try:
            handler = self.event_handlers[event.name()]
            getattr(self, handler)(event)
        except KeyError:
            pass

    def handle_command(self, command):
        try:
            handler = self.command_handlers[command.command_name()]
            getattr(self, handler)(command)
        except KeyError:
            pass

    def _on_signed_up(self, event):
        self._signed_up = True

    def sign_up(self, command):
        if self._signed_up:
            raise ValidationError(username="not_unique")

        for field in ['name', 'email', 'password', 'username']:
            if getattr(command, field) == '':
                raise ValidationError(*{field: "required"})

        self.events.publish(Event('user.signed-up', {
            'username': command.username,
            'aggregate_id': self.id,
            'password': command.password,
            'email': command.email,
            'name': command.name,
        }))

        return self


SignUp = namedtuple('SignUp', [
    'username',
    'password',
    'email',
    'name',
])

SignUp.Aggregate = User
SignUp.command_name = lambda self: 'sign-up'
SignUp.aggregate_id = lambda self: self.username
