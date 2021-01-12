from flask import render_template, url_for, flash, redirect, request, abort
from prod_break import app, bcrypt, db  # imports from __init__.py
from prod_break.forms import RegistrationForm, LoginForm, UpdateProfileForm
from prod_break.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required

from datetime import date, timedelta

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('task'))
    return render_template("home.html", title="home.")
    # return render_template("register.html", title="register.")
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
@login_required
def task():
    tasks = current_user.user_tasks
    cur_date = date.today()
    if cur_date > current_user.last_task_completed.date():
        current_user.daily_completed_tasks = 0
    for task in tasks:
        if task.date_completed and cur_date > task.date_completed.date():
            delete_task(task.id)
    return render_template("tasks.html", title=f"{current_user.username}'s tasks.", tasks=tasks, cur_date=cur_date)


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


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    user_pfp = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template("profile.html", title=f"{current_user.username}'s profile.", user_pfp=user_pfp, form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/tasks/add_task', methods=["GET","POST"])
@login_required
def add_task():
    task_input = request.form.get('task-txt')
    task_due = request.form.get('task-due')
    if task_input == '':
        return redirect(url_for('task'))
    if task_due:
        new_task = Task(task_name = task_input, user_id = current_user.id, due_date = date.fromisoformat(task_due))
    else:
        new_task = Task(task_name = task_input, user_id = current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task'))

@app.route('/tasks/delete_task/<int:task_id>', methods=["GET","POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash("this task is not available for you to delete.", "danger")
        return redirect(url_for('task'))
    db.session.delete(task)
    db.session.commit()
    # if not new_day:
    return redirect(url_for('task'))

@app.route('/tasks/complete_task/<int:task_id>', methods=["GET","POST"])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash("this task is not available for you to complete.", "danger")
        return redirect(url_for('task'))
    task.complete = not task.complete
    task.date_completed = date.today()
    current_user.last_task_completed = date.today()
    if task.complete:
        current_user.daily_completed_tasks += 1
    else:
        current_user.daily_completed_tasks -= 1
    db.session.commit()
    return redirect(url_for('task'))

@app.route('/profile/change_pfp/<string:new_pfp>', methods=["GET","POST"])
def change_pfp():
    db.session.commit()
    return redirect(url_for('profile'))