import sys

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, abort
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, DrugClass, Drug, NewDrugs, User
from forms import RegistrationForm, LoginForm, UpdateAccountForm, AddDrugForm, EditDrugForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, user_logged_out, login_required
from save_picture import save_profile_picture
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string


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


@app.route("/<drug_class>")
@login_required
def show_drugs(drug_class):
    drug_classes = session.query(DrugClass).filter_by(name=drug_class)
    drugs = session.query(Drug).filter_by(drug_class_name=drug_class)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('drugs.html', image_file=image_file, drug_class=drug_class,
                           drugs=drugs, drugclasses=drug_classes)


@app.route("/Newdrugs")
@login_required
def new_drugs():
    drugs = session.query(NewDrugs).order_by(asc(NewDrugs.name))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('new_drugs.html', drugs=drugs, image_file=image_file)


@app.route("/<drug_class>/<drug>/edit", methods=['GET', 'POST'])
@login_required
def edit_drug(drug_class, drug):
    drug_to_edit = session.query(Drug).filter_by(name=drug).one()
    form = EditDrugForm()

    if form.submit.data:
        if form.validate_on_submit():
            drug_to_edit.name = form.name.data
            drug_to_edit.drug_class_name = form.drug_class.data
            drug_to_edit.information = form.drug_info.data
            session.commit()
            flash('Drug has been updated!', 'success')
            return redirect(url_for('show_drugs', drug_class=drug_class))
    elif request.method == 'GET':
        form.name.data = drug_to_edit.name
        form.drug_class.data = drug_to_edit.drug_class_name
        form.drug_info.data = drug_to_edit.information
    return render_template('edit_drug.html', form=form, drug=drug, drug_class=drug_class)


@app.route("/<drug_class>/<drug>/edit/delete", methods=['GET', 'POST'])
@login_required
def delete_drug(drug_class, drug):
    drug_to_delete = session.query(Drug).filter_by(name=drug).first()
    session.delete(drug_to_delete)
    session.commit()
    drug_class_to_delete = session.query(Drug).filter_by(drug_class_name=drug_class).first()
    if drug_class_to_delete:
        flash('Drug has been deleted!', 'success')
        return redirect(url_for('show_drugs', drug_class=drug_class))
    else:
        drug_class_to_delete = session.query(DrugClass).filter_by(name=drug_class).one()
        session.delete(drug_class_to_delete)
        session.commit()
        flash('Drug has been deleted!', 'success')
        return redirect(url_for('account'))


@app.route("/Newdrugs/<drug>/edit", methods=['GET', 'POST'])
@login_required
def edit_new_drug(drug):
    new_drug_to_edit = session.query(NewDrugs).filter_by(name=drug).one()
    form = EditDrugForm()
    if form.validate_on_submit():
        new_drug_to_edit.name = form.name.data
        new_drug_to_edit.drug_class = form.drug_class.data
        new_drug_to_edit.information = form.drug_info.data
        session.commit()
        flash('Drug has been updated!', 'success')
        return redirect(url_for('new_drugs'))
    elif request.method == 'GET':
        form.name.data = new_drug_to_edit.name
        form.drug_class.data = new_drug_to_edit.drug_class
        form.drug_info.data = new_drug_to_edit.information
    return render_template('edit_new_drug.html', form=form, drug=drug)


@app.route("/Newdrug/<drug>edit/delete", methods=['GET', 'POST'])
@login_required
def delete_new_drug(drug):
    new_drug_to_delete = session.query(NewDrugs).filter_by(name=drug).first()
    session.delete(new_drug_to_delete)
    session.commit()
    flash('Drug has been deleted!', 'success')
    return redirect(url_for('new_drugs'))


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
            next_page = request.args.get('next')
            flash('Welcome %s!' % user.username, 'success')
            return redirect(next_page) if next_page else redirect(url_for('account'))
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


def save_picture(form_picture):
    return save_profile_picture(form_picture)


@app.route("/edit_account", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('edit_account.html', image_file=image_file, form=form)


@app.route("/drug/add", methods=['GET', 'POST'])
@login_required
def add_drug():
    form = AddDrugForm()
    if form.validate_on_submit():
        if form.recent_drug.data is True:
            new_drug = NewDrugs(name=form.name.data, drug_class=form.drug_class.data,
                                user_id=current_user.id, information=form.drug_info.data)
            session.add(new_drug)
            session.commit()
            flash('Drug has been added to New Drugs list!', 'success')
            return redirect(url_for('account'))
        # TO DO: find out why it's not adding drug if its not a new drug!
        elif form.recent_drug.data is False:
            drug = Drug(name=form.name.data, drug_class_name=form.drug_class.data,
                            user_id=current_user.id, information=form.drug_info.data)

            session.add(drug)
            session.commit()
            drug_class_exists = session.query(DrugClass).filter_by(name=form.drug_class.data).first()
            if drug_class_exists:
                flash('Drug has been added!', 'success')
                return redirect(url_for('account'))
            else:
                drug = DrugClass(name=form.drug_class.data, user_id=current_user.id)
                session.add(drug)
                session.commit()
                flash('Drug has been added!', 'success')
                return redirect(url_for('account'))
        return redirect(url_for('account'))
    return render_template('add_drug.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
