# Never gonna give you up!

# https://hackers.gg/challenges/web/realistic1/
# Attempting to decode the flask session cookie. Turns out it's way easier than the code below...
# https://blog.miguelgrinberg.com/post/how-secure-is-the-flask-user-session
# import base64
# import zlib
# s = ''
# # print(base64.urlsafe_b64decode(s))
# print(zlib.decompress(base64.urlsafe_b64decode(s)))


import flask.helpers
import flask.sessions
import itsdangerous

cookie_name = 'session'
cookie_value = ''

secret_key = 'drones'
secret_key = 'drone'


def open_session_original(self, app, request):
    s = self.get_signing_serializer(app)
    if s is None:
        return None
    val = request.cookies.get(app.session_cookie_name)
    if not val:
        return self.session_class()
    max_age = flask.helpers.total_seconds(app.permanent_session_lifetime)
    try:
        data = s.loads(val, max_age=max_age)
        return self.session_class(data)
    except itsdangerous.BadSignature:
        return self.session_class()


def get_signing_serializer_original(self, app):
    if not app.secret_key:
        return None
    signer_kwargs = dict(
        key_derivation=self.key_derivation,
        digest_method=self.digest_method
    )
    return itsdangerous.URLSafeTimedSerializer(app.secret_key, salt=self.salt,
                                               serializer=self.serializer,
                                               signer_kwargs=signer_kwargs)


def open_session_modified(self, app, request):
    s = self.get_signing_serializer(self, app)
    if s is None:
        return None
    val = cookie_value
    if not val:
        return self.session_class()
    max_age = flask.helpers.total_seconds(app.permanent_session_lifetime)
    try:
        data = s.loads(val, max_age=max_age)
        return self.session_class(data)
    except itsdangerous.BadSignature:
        return self.session_class()


def get_signing_serializer_modified(self, app):
    if not secret_key:
        return None
    signer_kwargs = dict(
        key_derivation=self.key_derivation,
        digest_method=self.digest_method
    )
    return itsdangerous.URLSafeTimedSerializer(secret_key, salt=self.salt,
                                               serializer=self.serializer,
                                               signer_kwargs=signer_kwargs)


app = flask.Flask(__name__)
app.secret_key = secret_key

with app.test_request_context('/?name=Peter'):
    assert flask.request.path == '/'
    assert flask.request.args['name'] == 'Peter'

    print(app)

    s = flask.sessions.SecureCookieSessionInterface()  # import flask.sessions
    # session.get_signing_serializer_modified = get_signing_serializer_modified
    s.open_session = open_session_modified
    s.get_signing_serializer = get_signing_serializer_modified
    s.open_session(s, app, flask.request)
    print(s)
    print(dir(s))

    # print(flask.session)
    # print(flask.session['session'])
