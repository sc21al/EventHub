from flask_bcrypt import bcrypt
from flask import Blueprint, redirect, session, url_for, render_template, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms.forms import LoginForm, RegistrationForm
from app.models.models import User
from app.extensions import bcrypt

# Create a Blueprint for user authentication views
userauth_dp = Blueprint("userauth_views", __name__, template_folder="../templates", static_folder="../static")

# After each request, modify the response to disable caching
@userauth_dp.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


# Route for user signup
@userauth_dp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Redirect authenticated users to the home page
    if current_user.is_authenticated:
        return redirect(url_for('general_views.home'))
    
    # Create a registration form instance
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate a hashed password and create a new user instance
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        # Add the new user to the database and commit the session
        db.session.add(user)
        db.session.commit()
        #flash of successful account creation and redirect to login
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('userauth_views.login'))
    else:
        print(form.errors) #Debugging line
    # Render the signup template
    return render_template('signup.html', form=form, title="Register")


# Route for user login
@userauth_dp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('general_views.home'))
    
    # Create a login form instance
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Attempt to retrieve the user from the database
            user = User.query.filter_by(username=form.username.data).first()
            # Verify the password and log the user in if valid
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                # Store the user ID in the session
                session['user_id'] = user.id 
                # Redirect to the next page or home page
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('general_views.home'))
            else:
                # If login is unsuccessful, notify the user
                flash('Login Unsuccessful. Please check username and password', 'danger')
        # Handle unexpected errors gracefully
        except Exception as e:
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
    # Render the login template        
    return render_template('login.html', form=form, title="Login")


#Route for user logout
@userauth_dp.route('/logout')
@login_required
def logout():
    # Log the user out and clear their session
    logout_user()
    session.pop('user_id', None)  
    # Flash successful logout and redirect to the home page
    flash('You have been logged out.', 'info')
    return redirect(url_for('general_views.home'))