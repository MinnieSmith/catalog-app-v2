import random
import string

from flask import Flask, url_for, render_template, redirect, flash
from flask_dance import OAuth2ConsumerBlueprint
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

blueprint = make_google_blueprint(
    client_id="538195736623-n1rglhdjfim8gnf32q0a9csg3jojhivs.apps.googleusercontent.com",
    client_secret="KC-Mk5cWr7Pl8yLikK5Bnyjn",
    redirect_to="account",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email"
    ]
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('test.html')


@app.route("/login",  methods=['GET', 'POST'])
def gconnect():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])


@app.route("/account",  methods=['GET', 'POST'])
def account():
    return render_template('test2.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
