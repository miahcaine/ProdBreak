from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
import email_validator
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from prod_break.models import User
from prod_break import bcrypt

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    conf_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('start logging tasks')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('this username is taken :( please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('this email already exists :( please choose a different one')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('login.')

class UpdateProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('update profile')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and username.data != current_user.username:
            raise ValidationError('this username is taken :( please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and email.data != current_user.email:
            raise ValidationError('this email already exists :( please choose a different one')