from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from database import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Route for user signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        is_therapist = int(request.form.get('is_therapist', 0))  # Get therapist status from form data
        therapist_email = request.form['therapist_email']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'error')
            return render_template('signup.html')

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(email=email, password_hash=hashed_password, first_name=first_name, last_name=last_name, is_therapist=is_therapist, therapist_email=therapist_email)
    
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        if new_user.is_therapist:
            return redirect('/therapist_dashboard')
        else:
            return redirect(url_for('profile'))

    return render_template('signup.html')

# Route for user login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.is_therapist:
                return redirect('/therapist_dashboard')
            else:
                return redirect(url_for('profile'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')

    return render_template('login.html')

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

