from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "7be87f5097974366dfe642c7f0c0b608"  # from built-in secrets module

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


if __name__ == "__main__":
    app.run(debug=True)