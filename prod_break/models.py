from prod_break import db, login_manager  # imports from __init__.py
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # inherits from database model and session manager
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    user_tasks = db.relationship("Task", backref="user", lazy=True)  # creates relationship between a user and their tasks

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Task('{self.task_name}', '{self.date_created}')"