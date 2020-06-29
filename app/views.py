# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging
import json

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm
from app.functions import loginPortal

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template( 'pages/register.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template( 'pages/register.html', form=form, msg=msg )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str) 
        
        msg = 'Please approve login via iOS app.'

        aka_user, status = loginPortal(username)

        # the idea here is that the loginPortal function will return the status and user information. 
        # the user info will be used to create a new user with that username. Upon logout happening, that user's account will be deleted(?)
        # so that upon new login, the account will be refreshed with new data from aka.
        
        if status == "Successfully got user data":
            db.drop_all()
            db.create_all()

            name = aka_user['name']
            email = aka_user['email']
            aka = aka_user['aka']
            phone = aka_user['phone']
            shippingAddress = aka_user['shippingAddress']
            billingAddress = aka_user['billingAddress']
            ageGroup = aka_user['ageGroup']
            gender = aka_user['gender']
            country = aka_user['country']
            dob = aka_user['dateOfBirth']

            #pref = json.dumps(aka_user['preferences'])

            user = User(name, 
                        email,
                        aka,
                        phone,
                        shippingAddress,
                        billingAddress,
                        ageGroup,
                        gender,
                        country,
                        dob)

            user.save()

            login_user(user)

            return redirect(url_for('index'))
        else:
            msg = "Unknown user"

    return render_template( 'pages/login.html', form=form, msg=msg ) 

# # Original Authenticate user
# @app.route('/login.html', methods=['GET', 'POST'])
# def login():
    
#     # Declare the login form
#     form = LoginForm(request.form)

#     # Flask message injected into the page, in case of any errors
#     msg = None

#     # check if both http method is POST and form is valid on submit
#     if form.validate_on_submit():

#         # assign form data to variables
#         username = request.form.get('username', '', type=str)
#         password = request.form.get('password', '', type=str) 

#         # filter User out of database through username
#         user = User.query.filter_by(user=username).first()

#         if user:
            
#             #if bc.check_password_hash(user.password, password):
#             if user.password == password:
#                 login_user(user)
#                 return redirect(url_for('index'))
#             else:
#                 msg = "Wrong password. Please try again."
#         else:
#             msg = "Unknown user"

#     return render_template( 'pages/login.html', form=form, msg=msg ) 

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # @WIP to fix this
        # Temporary solution to solve the dependencies
        if path.endswith(('.png', '.svg' '.ttf', '.xml', '.ico', '.woff', '.woff2')):
            return send_from_directory(os.path.join(app.root_path, 'static'), path)    

        # try to match the pages defined in -> pages/<input file>
        return render_template( 'pages/'+path )

    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )
