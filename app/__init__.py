from flask import Flask
from flask_restful import Api
from app.extensions import db, migrate, login_manager, admin, babel
from config import config

#Creates a Flask app
def create_app(config_name='default'):
    app = Flask(__name__)
    # Load the configuration from the 'config' dictionary
    app.config.from_object(config[config_name])

    # Initialize the extensions with the created Flask app 
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'userauth_views.login'
    admin.init_app(app)
    babel.init_app(app)

    from app.models.models import User, Event
    # Define the user_loader callback for Flask-Login which loads a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize Flask-RESTful API
    api = Api(app)

    # Initialize Flask-Admin views for User and Event models
    from app.views.admin import UserAdmin, EventAdmin
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(EventAdmin(Event, db.session))

    # Registering blueprints
    from app.views.user import user_dp
    from app.views.userauth import userauth_dp
    from app.views.events import events_dp
    from app.views.admin import admin_dp
    from app.views.general import general_dp

    app.register_blueprint(user_dp)        # User routes, profile routes
    app.register_blueprint(userauth_dp)    # User authentication routes, sign up / log in routes
    app.register_blueprint(events_dp)      # Event routes
    app.register_blueprint(admin_dp)       # Admin routes
    app.register_blueprint(general_dp)     # General routes (home page)

    # Import and register the RESTful resource
    from app.resources.like_event import LikeEvent
    from app.resources.join_event import JoinEvent
    api.add_resource(LikeEvent, '/like-event/<int:event_id>')  # Endpoint for liking an event
    api.add_resource(JoinEvent, '/join-event/<int:event_id>')  # Endpoint for joining an event

    return app
