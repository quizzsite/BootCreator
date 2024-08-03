from flask import Blueprint, render_template

from .models import User
from .forms import *
from .ext import projMan

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
    return render_template('iframe.html')

@main.route('/editor/<string:proj>')
def editorProject(proj):
    file = "index.html"
    src = projMan.update(proj, file, f"Save {file}")
    return render_template('editor.html', iframesrc=src, file=file)

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

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # Не используйте простой текст для паролей в реальных приложениях
            flash('Login successful', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)