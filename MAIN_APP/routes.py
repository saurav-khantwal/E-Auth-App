from crypt import methods
from MAIN_APP import app
from flask import render_template, url_for, flash, redirect, request, session
from MAIN_APP.forms import Register_form, Login_form, Otp_Register_form, Otp_Login_form
from datetime import datetime
import requests


server_ip_user = "http://127.0.0.1:8000/users"
server_ip_user_otp = "http://127.0.0.1:8000/users/otp"
server_ip_login = "http://127.0.0.1:8000/login"
server_ip_login_otp = "http://127.0.0.1:8000/login/otp"


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = Login_form()

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "password": form.password.data
        }


        server_return = requests.post(server_ip_login, json=data)

        if server_return.status_code == 404:

            if server_return.json()['detail'] == "Invalid username":
                flash(f'Invalid Username', category='danger')

            if server_return.json()['detail'] == "Invalid password":
                flash(f'Ivalid Password', category='danger')
        else:
            session['dict'] = server_return.json()
            return redirect(url_for('login_otp_page'))

    return render_template('login.html', form = form)


@app.route('/login/otp', methods=['GET', 'POST'])
def login_otp_page():
    form = Otp_Login_form()

    if form.validate_on_submit():

        payload = session['dict']
        data = {
            "username": payload["username"],
            "password": payload['password'],
            "otp": payload['otp'],
            "input_otp": form.otp.data
        }

        server_return = requests.post(server_ip_login_otp, json=data)

        if server_return.status_code == 404:
            flash('Wrong OTP', category='danger')

        else:
            flash('Successfully logged In', category='success')
            return redirect(url_for('home_page'))

    return render_template('otp_login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = Register_form()

    if form.validate_on_submit():

        data = {
        "username": form.username.data,
        "email": form.email_address.data,
        "password": form.password1.data
        }
        server_return = requests.post(server_ip_user, json=data)

        if server_return.status_code == 208:
            if server_return.json()['detail'] == "email already exists":
                flash(f'User with Email Already exists', category='danger')

            if server_return.json()['detail'] == "username already exists":
                flash(f'User with Username already exists', category='danger')

        else:
            session['dict'] = server_return.json()
            return redirect(url_for('register_otp_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating your account: {err_msg}', category='danger')

    return render_template('register.html', form = form)



@app.route('/register/otp', methods=['GET', 'POST'])
def register_otp_page():
    form = Otp_Register_form()

    payload = session['dict']

    if form.validate_on_submit():
        print("working")
        data = {
            'user': {
                'username': payload['user']['username'],
                'email': payload['user']['email'], 
                'password': payload['user']['password']
            },
            'otp': payload['otp'],
            'input_otp': form.otp.data
        }

        server_return = requests.post(server_ip_user_otp, json=data)

        if server_return.status_code == 404:
            flash(f'Wrong Otp', category='danger')

        else:
            print("This is working")
            flash(f'Registration Successfull', category='success')
            return redirect(url_for('home_page'))

    return render_template('otp_register.html', form = form)

