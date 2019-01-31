from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, abort
from flask import session as login_session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.google import make_google_blueprint, google
from blinker import Namespace

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, DrugClass, Drug, NewDrugs, User, OAuth
from forms import RegistrationForm, LoginForm, UpdateAccountForm, AddDrugForm, EditDrugForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, user_logged_out, login_required
from save_picture import save_profile_picture
import json
import random
import string

app = Flask(__name__)
engine = create_engine('sqlite:///drugcatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
bcrypt = Bcrypt(app)
my_signals = Namespace()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

blueprint = make_google_blueprint(
    client_id="538195736623-n1rglhdjfim8gnf32q0a9csg3jojhivs.apps.googleusercontent.com",
    client_secret="KC-Mk5cWr7Pl8yLikK5Bnyjn",
    redirect_to="account",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)
app.register_blueprint(blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "google.login"
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))


blueprint.backend = SQLAlchemyBackend(OAuth, session, user=current_user)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('test.html')


@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("failed to log in with Google.", "error")
        return False

    resp = blueprint.session.get("/user")
    if not resp.ok:
        flash("failed to fetch user info from Google.", "error")
        return False

    google_info = resp.json()
    google_id = str(google_info["id"])
    image_file = "https://www.google.com/s2/photos/profile/{google_id}"

    try:
        oauth = session.query(OAuth).filter_by(provider=blueprint.name, provider_user_id=google_id)
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=google_id, token=token, image_file=image_file)
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google", "success")
    return False


@oauth_error.connect_via(blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")


@app.route("/account",  methods=['GET', 'POST'])
def account():
    return render_template('test2.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
