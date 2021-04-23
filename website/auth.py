from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist!', category='error')
        elif len(email) < 4:
            flash('Email is not valid!', category='error')
        elif len(firstName) < 2:
            flash('First name should contain more than 2 characters!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 7:
            flash('Password length should be greater that 7 characters!', category='error')
        else:
            # add user to db
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Sign Up successful', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
