from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField

# Create a Blueprint for admin views
admin_dp = Blueprint("admin_views", __name__, template_folder="../templates/admin", static_folder="../static")

# After each request, disable caching to prevent sensitive information from being stored
@admin_dp.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


# Route for admin dashboard
@admin_dp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # Redirect non-admin users to the home page
    if not current_user.is_admin:
        return redirect(url_for('home'))  # Redirect to a public page
    return render_template('admin_dashboard.html')


# Standalone _list_formatter function
def _list_formatter(view, context, model, name):
    items = getattr(model, name)
    return ', '.join([str(item) for item in items])


# Define UserAdmin view for Flask-Admin
class UserAdmin(ModelView):
    column_list = ('username', 'email', 'created_events', 'liked_events', 'joined_events')
    column_searchable_list = ('username', 'email')
    form_columns = ('username', 'email', 'password')
    form_extra_fields = {'password': PasswordField('New Password')}


    # Override on_model_change to handle password changes
    def on_model_change(self, form, model, is_created):
        # Hash new password before saving to the database
        if form.password.data:
            model.set_password(form.password.data)


    # Custom column formatters
    def _list_formatter(view, context, model, name):
        items = getattr(model, name)
        return ', '.join([str(item) for item in items])

    # Custom column formatters
    column_formatters = {
        'created_events': _list_formatter,
        'liked_events': _list_formatter,
        'joined_events': _list_formatter,
    }


    # Redirect to login page if user is not authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('userauth_views.login', next=request.url))


# Define EventAdmin view for Flask-Admin
class EventAdmin(ModelView):
    # Exclude participants from the list and form views for simplicity
    column_exclude_list = ['participants']  # Exclude participants from the list view
    form_excluded_columns = ['participants']  # Exclude from the form
    # Enable search on 'title' and 'category' fields
    column_searchable_list = ('title', 'category')

    # Redirect to login page if user is not authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('userauth_views.login', next=request.url))
    

    # Standalone function to format list items for Flask-Admin columns
def _list_formatter(view, context, model, name):
    # Return a comma-separated string of items
    items = getattr(model, name)
    return ', '.join([str(item) for item in items])