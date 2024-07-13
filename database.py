from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False, default=0)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    father_name = db.Column(db.String(100), nullable=True)
    mother_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(20), nullable=True)
    is_therapist = db.Column(db.Boolean, nullable=False, default=False)
    therapist_email = db.Column(db.String(100), nullable=False)

# Define Score model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_stories_score = db.Column(db.Integer, default=0)
    total_correct_stories_score = db.Column(db.Integer, default=0)
    total_grammar_score = db.Column(db.Integer, default=0)
    total_correct_grammar_score = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('scores', lazy=True))

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref=db.backref('audio_files', lazy=True))