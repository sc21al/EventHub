
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, DateField, TimeField, SubmitField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp

# Form for creating a new event.
class CreateEventForm(FlaskForm):
    # Fields for event details with validators to ensure correct data entry.
    title = StringField('Title',validators=[DataRequired(), Length(max=255)])
    category = SelectField('Category', choices=[
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
        ('education', 'Education'),
        ('art', 'Art'),
        ('food', 'Food & Drink'),
        ('health', 'Health'),
        ('business', 'Business'),
        ('travel', 'Travel'),
        ('outdoors', 'Outdoors'),
        ('entertainment', 'Entertainment'),
        ], validators=[DataRequired()])   
    description = TextAreaField('Description', validators=[Length(max=500)])
    date = DateField('Date', format="%Y-%m-%d")
    start_time = TimeField('Start Time', format="%H:%M")
    end_time = TimeField('End Time', format="%H:%M")
    location = StringField('Location', validators=[Length(max=100)])
    submit = SubmitField('Create Event')

# Form for user registration with validation for username, email, and password.
class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    # Password field with regex validator for secure password requirements.
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Password must be at least 8 characters with one number, one uppercase and one lowercase letter.')
    ])
    submit = SubmitField('Register')

# Login form.
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# Update profile form.
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Password must be at least 8 characters with one number, one uppercase and one lowercase letter.')
    ])
    submit = SubmitField('Update')
