from flask import Blueprint, render_template, redirect
from flask_login import current_user

# Create a Blueprint for user views
general_dp = Blueprint("general_views", __name__, template_folder="../templates", static_folder="../static")

# Headers to each response to prevent caching
@general_dp.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


# Route for home page
@general_dp.route("/")
def home():
    return render_template("home.html", user=current_user, title='EventHub')
