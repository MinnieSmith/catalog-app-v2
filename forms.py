from flask_wtf import FlaskForm
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from database_setup import User, Base
from flask_login import current_user

engine = create_engine('sqlite:///drugcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username.')

    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = session.query(User).filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = session.query(User).filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

