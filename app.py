from flask import Flask, render_template,request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'secretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'shreyaspatil2712@gmail.com': 'password123'}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid username or password. Please try again.')
    
    return render_template('login.html')


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', name=current_user.id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/')
def hello_flask():
    return render_template("index.html")

@app.route('/bio')
def bio():
    details = {
        "name": "Shreyas Patil",
        "age": 20,
        "hobbies": ["Food", "Gaming", "Coding"]
    }
    return render_template("bio.html", details=details)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            result = num1 + num2
        except ValueError:
            result = "Invalid input. Please enter numeric values."
    return render_template("calculator.html", result=result)

tasks = []

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            tasks.append(task) 
        return redirect(url_for('todo'))  # avoid  resubmission
    return render_template("todo.html", tasks=tasks)


import random

quotes = [
    "Believe you can and you're halfway there.",
    "Act as if what you do makes a difference. It does.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Keep going. Everything you need will come to you at the perfect time.",
    "You don’t have to be perfect to be amazing.",
    "The only limit to our realization of tomorrow is our doubts of today."
]

@app.route('/quote')
def quote():
    random_quote = random.choice(quotes) 
    return render_template("quote.html", quote=random_quote)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

feedback_list = []

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        feedback_text = request.form.get('feedback')

        if name and feedback_text:
            feedback_list.append({'name': name, 'feedback': feedback_text})

        return redirect(url_for('feedback'))

    return render_template('feedback.html', feedback_list=feedback_list)

users = [
    {'name': 'Shreyas', 'age': 21, 'city': 'Pune'},
    {'name': 'Ajay', 'age': 50, 'city': 'Pune'},
    {'name': 'kevin', 'age': 20, 'city': 'Chennai'},
    {'name': 'Pihoo', 'age': 21, 'city': 'Delhi'},
    {'name': 'Kapil', 'age': 58, 'city': 'Hyderabad'},
]

@app.route('/users')
def users_table():
    return render_template('users.html', users=users)

@app.route('/converter', methods=['GET', 'POST'])
def converter():
    fahrenheit = None
    if request.method == 'POST':
        celsius = request.form.get('celsius')
        if celsius:
            try:
                celsius = float(celsius)
                fahrenheit = (celsius * 9/5) + 32
            except ValueError:
                fahrenheit = "Invalid input. Please enter a number."

    return render_template('converter.html', fahrenheit=fahrenheit)

if __name__ == '__main__':
    app.run(debug=True)

