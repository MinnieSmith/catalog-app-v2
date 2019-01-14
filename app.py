import sys

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DrugClass, Drug, DrugInformation, NewDrugs, NewDrugInformation
from forms import RegistrationForm, LoginForm
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

engine = create_engine('sqlite:///drugcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def home():
    drug_classes = session.query(DrugClass).order_by(asc(DrugClass.name))
    new_drugs = session.query(NewDrugs).order_by(asc(NewDrugs.name))
    return render_template('home.html', drugclasses=drug_classes, newdrugs=new_drugs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@drugcatalogapp.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
