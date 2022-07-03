from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Regexp



class Register_form(FlaskForm):
    # Registration form
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email address', validators=[Regexp('^[a-zA-Z]+[0-9]*@[a-z]+\.[a-z]+$', message='invalid email type'), DataRequired()])
    password1 = PasswordField(label='Password', validators=[DataRequired(),
     Regexp('^[a-zA-Z0-9]{6,12}$', message="Invalid use of characters in password")])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class Login_form(FlaskForm):
    #Login form
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class Otp_Login_form(FlaskForm):
    #Form for login otp
    otp = StringField(label="otp")
    submit = SubmitField(label='Submit')


class Otp_Register_form(FlaskForm):
    #form for registration otp
    otp = StringField(label="otp")
    submit = SubmitField(label='Submit')


class Profile_form(FlaskForm):
    # Profile Update form
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='Password', validators=[DataRequired(),
     Regexp('^[a-zA-Z0-9]{6,12}$', message="Invalid use of characters in password")])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Update Account')

