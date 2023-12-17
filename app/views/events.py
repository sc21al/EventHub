from flask import Blueprint, flash, render_template, redirect, url_for, jsonify, request
from flask_login import current_user, login_required
from app.forms.forms import CreateEventForm
from app.models.models import Event, User, likes, registrations
from app import db
from sqlalchemy import desc, func
from sqlalchemy.orm import aliased

# Blueprint
events_dp = Blueprint("events_views", __name__, template_folder="../templates/events", static_folder="../static")


# Add headers to each response to prevent caching for security reasons@events_dp.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


# Helper function to check if the current user is the creator of the event
def is_event_creator(event_id, user_id):
    return Event.query.filter_by(id=event_id, creator_id=user_id).first() is not None


# Route to display all events for exploration
@events_dp.route("/explore_event")
def explore_events():
    events = Event.query.all()  # Fetch all events from the database
    return render_template("explore_events.html", events=events, title="Explore Events")


# Route to display user's created and joined events
@events_dp.route('/my_events')
@login_required
def my_events():
    created_events = current_user.created_events
    joined_events = current_user.joined_events  # Convert to list
    recommended_event = recommendation()        # Get a recommended event
    return render_template("my_events.html", created_events=created_events, joined_events=joined_events, recommended_event=recommended_event, title="My Events")


# Route to create a new event
@events_dp.route("/create_event", methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        # Create new Event object with form data
        new_event = Event(
            title=form.title.data,
            category=form.category.data, 
            description=form.description.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            creator_id=current_user.id  # Set the creator_id to the current user's ID
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events_views.my_events'))
    return render_template("create_event.html", form=form, title="Create Event")


# Route to delete an event
@events_dp.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    if not is_event_creator(event_id, current_user.id):
        flash('You do not have permission to delete this event.', 'danger')
        return redirect(url_for('events_views.my_events'))
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events_views.my_events'))


# Route to edit an event
@events_dp.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Check if current user is the creator of the event
    if not is_event_creator(event_id, current_user.id):
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('events.my_events'))
    if event.creator_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('events_views.my_events'))
    
    # Check if current user is the creator of the event
    form = CreateEventForm(obj=event)  # Populate form with event data
    if form.validate_on_submit():
        # Update event details and save to the database
        event.title = form.title.data
        event.category = form.category.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.location = form.location.data
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events_views.my_events'))
    return render_template("edit_event.html", form=form, event=event, title="Edit Event")


# Route for event recommendation system
@events_dp.route('/recommendation')
@login_required
def recommendation():

    """
    This function implements the event recommendation system. It analyzes the user's
    engagement with events (likes and joins) to recommend an event that aligns with their
    interests. The recommendation is based on two key factors: activity in specific categories
    and overall event popularity.

   The process involves:
    1. Identifying the most active categories for the user based on their past interactions.
    2. Searching for an appropriate event in these categories that the user has not joined
       or created.
    3. If no specific event is found in these categories, fall back to the most liked unjoined, 
    not self-created event overall.
    """

    # Step 1: Determine the user's most active categories based on likes and joins
    # This query aggregates the user's activity (likes and joins) in each category
    # and orders them by the count of activities to find the categories with the highest engagement.
    # c means column in the SQLAlchemy
    most_active_categories = db.session.query(
        Event.category,
        func.count('*').label('activity_count')
    ).outerjoin(likes, Event.id == likes.c.event_id) \
    .outerjoin(registrations, Event.id == registrations.c.event_id) \
    .filter(
        (likes.c.user_id == current_user.id) | 
        (registrations.c.user_id == current_user.id)
    ).group_by(Event.category) \
    .order_by(desc('activity_count')) \
    .all()

    # Define the total_activity_subquery outside the loop
    # This subquery calculates the total activity (likes and joins) for each event,
    # which will be used to evaluate the event's overall popularity.
    total_activity_subquery = db.session.query(
        Event.id,
        (func.count(likes.c.user_id) + func.count(registrations.c.user_id)).label('total_activity')
    ).outerjoin(likes, Event.id == likes.c.event_id) \
    .outerjoin(registrations, Event.id == registrations.c.event_id) \
    .group_by(Event.id) \
    .subquery()

    # Step 2: Find an unjoined, not self-created event in these categories
    # Loop through the most active categories and find the first event that matches
    # the criteria of being unjoined by the user and not created by them, prioritizing
    # events with higher total activities.
    for category, _ in most_active_categories:
        recommended_event = db.session.query(Event) \
        .join(total_activity_subquery, Event.id == total_activity_subquery.c.id) \
        .filter(
            Event.category == category,
            Event.creator_id != current_user.id,
            ~Event.participants.any(User.id == current_user.id)
        ) \
        .order_by(desc(total_activity_subquery.c.total_activity)) \
        .first()

        if recommended_event:
            return recommended_event

    # Step 3: Fallback to the most liked unjoined, not self-created event overall
    # If no event is found in the user's active categories, this block recommends
    # the most popular event across all categories that the user has neither joined
    # nor created.
    recommended_event = db.session.query(Event) \
    .join(total_activity_subquery, Event.id == total_activity_subquery.c.id) \
    .filter(
        Event.creator_id != current_user.id,
        ~Event.participants.any(User.id == current_user.id)
    ) \
    .order_by(desc(total_activity_subquery.c.total_activity)) \
    .first()

    # Return the recommended event if found, otherwise return None
    return recommended_event if recommended_event else None
