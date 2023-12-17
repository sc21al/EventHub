from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

# Defines many-to-many relationship tables for likes and registrations between users and events.
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

# User model with fields and relationships to events they've created, liked, or joined.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Relationship definitions for created, liked, and joined events.
    created_events = db.relationship('Event', backref='creator', lazy=True)
    liked_events = db.relationship('Event', secondary=likes, backref=db.backref('liked_by', lazy='dynamic'))
    joined_events = db.relationship('Event', secondary=registrations, backref=db.backref('participants', lazy='dynamic'))

    # Methods for password management.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Representation method for printing the user object.
    def __repr__(self):
        return f'<User {self.username}>'

# Event model with fields for event properties.
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Representation method for printing the event object.
    def __repr__(self):
        return f'<Event: {self.title}>'