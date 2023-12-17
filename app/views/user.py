from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.extensions import bcrypt
from app import db
from app.forms.forms import UpdateProfileForm
from app.views.userauth import logout

# Create a Blueprint for user views
user_dp = Blueprint("user_views", __name__, template_folder="../templates/user", static_folder="../static")

# After each request, disable caching to prevent sensitive information from being stored
@user_dp.after_request
def add_no_cache(response):
    # Headers to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response

# Route for updating user profile
@user_dp.route("/update_profile", methods=['GET', 'POST'])
@login_required
def update_profile():
    # Prefill the form with the current user's information
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        print("Form submitted")  # Debug print
        # Update user details and save to the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        # If password is provided, hash it and update the user's password
        if form.password.data:
            current_user.password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('events_views.explore_events'))
    else:
        print("Form errors:", form.errors)  # Debug print
    return render_template("update_profile.html", form=form, title="Update Profile")


# Route for deleting user account
@user_dp.route("/delete_account", methods=['POST'])
@login_required
def delete_account():
    # Check if the current user is the owner of the account
    user = current_user
    if not user.is_owner_of_account():
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('some_route'))
    else:
        # Delete user account from the database and log them out
        db.session.delete(user)
        db.session.commit()
        logout()
        flash('Your account has been deleted!', 'success')
        return redirect(url_for('general_views.home')) 
