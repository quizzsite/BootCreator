from flask import Blueprint, render_template
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('iframe.html', users=users)

@main.route('/')
def home():
    return render_template('leftMenu.html')

@main.route('/editor')
def editor():
    return render_template('editor.html')

def registerUser(usr):
    if User.query.get(usr):
        usr.payed = True
    return 

@main.route('/test_db')
def test_db():
    try:
        result = User.query.all()
        return 'Database connection is working!'
    except Exception as e:
        return f'Database connection failed: {e}'
