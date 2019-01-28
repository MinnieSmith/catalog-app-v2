# Flask Imports
from flask import Flask, request, redirect, url_for, render_template, jsonify, flash, make_response
from flask import session as login_session
from flask import jsonify
import requests
# Database Imports
from database_setup import Base, User
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
# Utility Imports
import json
import random
import string
import httplib2
# Oauth2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

engine = create_engine('sqlite:///drugcatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


def gconnect():
    # Validate the State Token
    if request.args.get('state') != login_session['state']:
        flash('State token incorrect. Please try again.')
        return redirect(url_for('index'))

    code = request.data

    # Try to upgrade code
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Check for error in access
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check user permission
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Checking validity for App
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Checking current session
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Storing token in session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Fetching user information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    user_data = answer.json()

    user = session.query(User).filter_by(email=user_data['email']).first()

    if user is not None:
        login_session['user_id'] = user.id
        flash('Logged in as %s' % user.username)
        return 'User Logged in!'

    newuser = User(username=user_data['email'], email=user_data['email'])
    session.add(User)
    session.commit()
    user = session.query(User).filter_by(email=newuser.email).first()
    login_session['user_id'] = user.id
    flash('Logged in as %s' % user.username)

    return "Account Created. User now Logged in!"
