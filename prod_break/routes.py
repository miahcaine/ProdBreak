from flask import render_template, url_for, flash, redirect, request
from prod_break import app, bcrypt, db  # imports from __init__.py
from prod_break.forms import RegistrationForm, LoginForm
from prod_break.models import User, Task
from flask_login import login_user, current_user, logout_user

# tasks = [
#     {"date": "12-21-2020", "task_name": "get groceries", "complete": False},
#     {"date": "12-22-2020", "task_name": "walk dog", "complete": True},
#     {"date": "12-23-2020", "task_name": "exercise", "complete": False},
# ]


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    return render_template("home.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"your account has been created! you can now log in below.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="register.", form=form)


@app.route("/tasks", methods=["GET", "POST"])
def task():
    tasks = current_user.user_tasks
    return render_template("tasks.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('task'))
        else:    
            flash('login unsuccessful. please check username and password.', 'danger')
    return render_template("login.html", title="login.", form=form)


@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_task', methods=["GET","POST"])
def add_task():
    task_input = request.form.get('task-txt')
    if task_input == '':
        return redirect(url_for('task'))
    new_task = Task(task_name = task_input, user_id = current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task'))
