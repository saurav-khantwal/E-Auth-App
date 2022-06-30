from crypt import methods
from email.mime import message
from MAIN_APP import app
from flask import render_template, url_for, flash, redirect, request, session, g
from MAIN_APP.forms import Register_form, Login_form, Otp_Register_form, Otp_Login_form
from datetime import datetime
import requests
import base64



# Api route urls

server_ip_user = "http://127.0.0.1:8000/users"
server_ip_user_otp = "http://127.0.0.1:8000/users/otp"
server_ip_login = "http://127.0.0.1:8000/login"
server_ip_login_otp = "http://127.0.0.1:8000/login/otp"


# before request
@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        g.user = session['data']


# home page route
@app.route('/home')
def home_page():
    if not g.user:
        flash("You need to login before accessing this page", 'info')
        return redirect(url_for('login_page'))
    return render_template('home.html')



# Login page Route
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login_page():

    '''
        This route will take input from the login form and validate it.
    '''

    form = Login_form()

    # If the input data is in correct form
    if request.method == "POST":
        session.pop('user_id', None)
        if form.validate_on_submit():
            data = {
                "username": form.username.data,
                "password": form.password.data
            }


            # Sending request to the server to check the credentials
            server_return = requests.post(server_ip_login, json=data)

            # If invalid details are there is the credentials
            if server_return.status_code == 404:

                if server_return.json()['detail'] == "Invalid username":
                    flash(f'Invalid Username', category='danger')

                if server_return.json()['detail'] == "Invalid password":
                    flash(f'Ivalid Password', category='danger')

        # Else put the data in the session dictionary so that login_otp_page route can use the data.    
            else:   
                session['dict'] = server_return.json()
                return redirect(url_for('login_otp_page'))

    return render_template('login.html', form = form)





@app.route('/login/otp', methods=['GET', 'POST'])
def login_otp_page():
    form = Otp_Login_form()


    # If the input data is in correct form
    if form.validate_on_submit():

        # Here we are using session dictionary to use the data from the login_page route
        payload = session['dict']
        payload['input_otp'] = form.otp.data
        # data = {
        #     "username": payload["username"],
        #     "user_id": payload['user_id'],
        #     "password": payload['password'],
        #     "otp": payload['otp'],
        #     "input_otp": form.otp.data
            
        # }

        # Sending request to the api to check the otp
        server_return = requests.post(server_ip_login_otp, json=payload)

        if server_return.status_code == 404:
            flash('Wrong OTP', category='danger')

        else:
            session['access_token'] = server_return.json()['access_token']
            print(session['access_token'])
            session['user_id'] = payload['user_id']
            session['data'] = payload
            flash('Successfully logged In', category='success')
            return redirect(url_for('home_page'))

    return render_template('otp_login.html', form = form)



@app.route('/logout')
def logout_page():
    session.pop('user_id', None)
    return redirect(url_for('login_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = Register_form()

    # If the form data is in correct format
    if form.validate_on_submit():


        data = {
        "username": form.username.data,
        "email": form.email_address.data,
        "password": form.password1.data
        }

        # Sending the api request with the inputted data
        server_return = requests.post(server_ip_user, json=data)

        # If there is some problem with user credentials
        if server_return.status_code == 208:
            if server_return.json()['detail'] == "email already exists":
                flash(f'User with Email Already exists', category='danger')

            if server_return.json()['detail'] == "username already exists":
                flash(f'User with Username already exists', category='danger')
        
        # Else add data to session dictionary for its use in otp page.
        else:
            session['dict'] = server_return.json()
            return redirect(url_for('register_otp_page'))

    # If there are errors in some validations.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating your account: {err_msg}', category='danger')

    return render_template('register.html', form = form)




@app.route('/register/otp', methods=['GET', 'POST'])
def register_otp_page():
    form = Otp_Register_form()

    # Data from the session dictionary
    payload = session['dict']

    # If form data is in correct format
    if form.validate_on_submit():
        data = {
            'user': {
                'username': payload['user']['username'],
                'email': payload['user']['email'], 
                'password': payload['user']['password']
            },
            'otp': payload['otp'],
            'input_otp': form.otp.data
        }
        
        # Send the request to the api to check the otp
        server_return = requests.post(server_ip_user_otp, json=data)

        # If the otp is wrong
        if server_return.status_code == 404:
            flash(f'Wrong Otp', category='danger')

        else:
            print("This is working")
            flash(f'Registration Successfull', category='success')
            return redirect(url_for('home_page'))

    return render_template('otp_register.html', form = form)

