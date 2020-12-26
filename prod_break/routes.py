from flask import render_template, url_for, flash, redirect
from prod_break import app  # imports app from __init__.py
from prod_break.forms import RegistrationForm, LoginForm
from prod_break.models import User, Task

tasks = [
    {"date": "12-21-2020", "task_name": "get groceries", "complete": False},
    {"date": "12-22-2020", "task_name": "walk dog", "complete": True},
    {"date": "12-23-2020", "task_name": "exercise", "complete": False},
]


@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"account created for {form.username.data}!", "success")
        return redirect(url_for("task"))
    return render_template("register.html", title="register.", form=form)


@app.route("/tasks", methods=["GET", "POST"])
def task():
    return render_template("tasks.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'abc':
            flash('you have been logged in!', 'success')
            return redirect(url_for('task'))
        else:
            flash('login unsuccessful. please check username and password', 'danger')
    return render_template("login.html", title="login.", form=form)


@app.route("/profile")
def profile():
    return render_template("profile.html")
