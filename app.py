from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'you-will-never-guess')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab7.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif len(password) < 8 or not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password) or not re.search(r'\d$', password):
            flash('Password must be at least 8 characters long, contain a lowercase letter, an uppercase letter, and end with a number.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email Address already exists!', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
        else:
            user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                username=username,
                email=email
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('thankyou'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Clear flash messages before rendering
    get_flashed_messages()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            flash('Login successful!', 'success')
            return redirect(url_for('secretPage'))
        flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/secretPage')
def secretPage():
    return render_template('secretPage.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
