from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class Register_form(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    image = FileField(label="Add image")
    submit = SubmitField(label='Create Account')


class Login_form(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class Otp_Login_form(FlaskForm):
    otp = StringField(label="otp")
    submit = SubmitField(label='Submit')


class Otp_Register_form(FlaskForm):
    otp = StringField(label="otp")
    submit = SubmitField(label='Submit')




