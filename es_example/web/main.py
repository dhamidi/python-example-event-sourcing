from es_example import *
import es_example.projection as projection
from bottle import route, run, template, request

class Projections:
    def __init__(self, filename):
        self._filename = filename
        self.all_users = projection.AllUsers()
        self.all_users.load(self._filename)

    def handle_event(self, event):
        self.all_users.handle_event(event)
        self.all_users.persist(self._filename)

EVENT_STORE = EventsOnDisk("events.db")
APP = Application(EVENT_STORE)
PROJECTIONS = Projections('projections.db')
EVENT_STORE.replay_all(PROJECTIONS)
APP.add_event_handler(PROJECTIONS)

@route("/users")
def list_users():
    users = PROJECTIONS.all_users.index()
    return template("""
<ul>
 % for user in users:
 <li>{{user.name}}</li>
 % end
</ul>
    """, users=users)

@route("/sign-up", method="POST")
def sign_up_user():
    fields = ['username', 'name', 'email', 'password']
    command = SignUp(**{key: request.forms.get(key) for key in fields})
    result = APP.handle_command(command)

    if result != True:
        return result.fields

@route("/sign-up", method="GET")
def show_signup_form():
    return """
<form action="/sign-up" method="POST">
  <p>
    <label>Username: <input name="username" type="text"></label>
  </p>
  <p>
    <label>Your name: <input name="name" type="text"></label>
  </p>
  <p>
    <label>Password: <input name="password" type="password"></label>
  </p>
  <p>
    <label>Email: <input name="email" type="text"></label>
  </p>
  <p>
    <button type="submit">Sign up</button>
  </p>
</form>
"""

run(host='localhost', port=8080, debug=True, reloader=True)
