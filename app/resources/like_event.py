from flask_restful import Resource
from flask_login import current_user, login_required
from app.extensions import db
from app.models.models import Event
from flask import jsonify, redirect, request, url_for


# Resource for liking an event, requires user to be logged in.
class LikeEvent(Resource):
    @login_required  
    def post(self, event_id):

        # Check if the user is authenticated, provide JSON response if unauthorized.
        if not current_user.is_authenticated:

            # Handle AJAX request differently from standard request.
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

                return jsonify({'status': 'unauthorized'}), 401
            # Redirect to login page if not an AJAX request.
            return redirect(url_for('userauth_views.login'))
        
        # Retrieve the event or return a 404 error if not found.
        event = Event.query.get_or_404(event_id)

        # Toggle the like status of the event for the current user.
        if current_user in event.liked_by:
            event.liked_by.remove(current_user)
            liked = False
        else:
            event.liked_by.append(current_user)
            liked = True

        # Save the changes to the database.
        db.session.commit()
        
        # Return the like status and count as JSON.
        return jsonify({'status': 'success', 'liked': liked, 'likes': event.liked_by.count()})
