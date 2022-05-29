from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flaskapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    contact = StringField('Contact Number',
                          validators=[DataRequired(), Length(10)])
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is already registered.')

    def validate_contact(self, contact):
        contact = User.query.filter_by(contact=contact.data).first()
        if contact:
            raise ValidationError('This contact number is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LOGIN')


class UpdateAccountForm(FlaskForm):
    username = StringField('Full Name',
                           validators=[Length(min=2, max=25)])
    contact = StringField('Contact Number',
                          validators=[Length(10)])
    email = StringField('Email Address',
                        validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('EDIT PROFILE')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('REQUEST PASSWORD CHANGE')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account registered with this email. Please Register!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('RESET PASSWORD')

