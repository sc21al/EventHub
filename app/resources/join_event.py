from flask_restful import Resource
from flask_login import login_required, current_user
from app.extensions import db
from app.models.models import Event
from flask import jsonify, request, redirect, url_for


# Resource for joining or unjoining an event, requires user to be logged in.
class JoinEvent(Resource):
    @login_required  # Ensure user is logged in.
    def post(self, event_id):
        if not current_user.is_authenticated: # Check if the user is authenticated, provide JSON response if unauthorized.
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest': # Handle AJAX request differently from standard request.
                return jsonify({'status': 'unauthorized'}), 401
            return redirect(url_for('userauth_views.login'))  # Redirect to login page if not an AJAX request.
              
        # Retrieve the event or return a 404 error if not found.
        event = Event.query.get_or_404(event_id)
        joined = False  # Default join status.

        # Toggle the participant status of the event for the current user.
        if current_user in event.participants:
            event.participants.remove(current_user)
        else:
            event.participants.append(current_user)
            joined = True

        # Save the changes to the database.
        db.session.commit()

        # Return the join status and count as JSON.
        return jsonify({'status': 'success', 'joined': joined, 'participants': event.participants.count()})