from flask import Flask, render_template

app = Flask(__name__)

tasks = [
    {
        'date':'12-21-2020',
        'task_name' : 'get groceries',
        'complete' : False
    },
    {
        'date':'12-22-2020',
        'task_name' : 'walk dog',
        'complete' : True
    },
    {
        'date':'12-23-2020',
        'task_name' : 'exercise',
        'complete' : False
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', tasks = tasks)

@app.route('/tasks')
def about():
    return render_template('tasks.html', tasks = tasks)

if __name__ == "__main__":
    app.run(debug=True)