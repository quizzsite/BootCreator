from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_caching import Cache
from celery import Celery, Task, shared_task

from config import Config
from .models import *
from .ext import *
from .routes import main

#App
app = Flask(__name__)
app.config.from_object(Config)

celery_init_app(app)
db.init_app(app)
appServer.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)

@appServer.on('send_data')
def handle_data(data):
    emit('receive_data', {'result': "result"})

@app.route('/')
def home():
    return render_template('leftMenu.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

def registerUser(usr):
    if User.query.get(usr):
        usr.payed = True
    return 

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b

@app.route('/test_db')
def test_db():
    try:
        result = User.query.all()
        return 'Database connection is working!'
    except Exception as e:
        return f'Database connection failed: {e}'


def runServ():
    appServer.run(app, debug=True)

if __name__ == "__main__":
    runServ()