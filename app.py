import sys

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DrugClass, Drug, DrugInformation, NewDrugs, NewDrugInformation, User
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, user_logged_out, login_required
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
from flask import make_response
from flask import session as login_session
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

engine = create_engine('sqlite:///drugcatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))


@app.route("/")
def home():
    drug_classes = session.query(DrugClass).order_by(asc(DrugClass.name))
    new_drugs = session.query(NewDrugs).order_by(asc(NewDrugs.name))
    return render_template('home.html', drugclasses=drug_classes, newdrugs=new_drugs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        session.add(user)
        session.commit()
        flash(f'Your account has been created! You are able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    drug_classes = session.query(DrugClass).order_by(asc(DrugClass.name))
    new_drugs = session.query(NewDrugs).order_by(asc(NewDrugs.name))
    return render_template('account.html', drugclasses=drug_classes, newdrugs=new_drugs,
                           image_file=image_file)


@app.route("/edit_account", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('edit_account.html', image_file=image_file, form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
