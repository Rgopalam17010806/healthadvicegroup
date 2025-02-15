import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import logging

logging.basicConfig(level=logging.INFO)

auth = Blueprint('auth', __name__)

#login route 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # logging.info(f"Login attempt for email: {email}")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                logging.warning("Incorrect password")
                flash('Incorrect password, try again.', category='error')
        else:
            logging.warning("Email does not exist")
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

#logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dateofbirth = request.form.get('dateofbirth')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check for none values
        if not email or not first_name or not last_name or not password1 or not password2:
            flash('Please fill out all of the fields.', category='error')
            return redirect(url_for('auth.signup'))
        
        try:
            dateofbirth = datetime.datetime.strptime(dateofbirth, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use 'YYYY-MM-DD'", category='error')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                dateofbirth=dateofbirth,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)