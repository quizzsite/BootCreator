from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from celery import Celery, Task, shared_task

from config import Config

#App
app = Flask(__name__)
app.config.from_object(Config)

#Socketio
appServer = SocketIO(app)

#SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)

with app.app_context():
    db.create_all()

celery_init_app(app)

@appServer.on('send_data')
def handle_data(data):
    emit('receive_data', {'result': "result"})

@app.route('/')
def home():
    return render_template('leftMenu.html')

@app.route('/editor')
def editor():
    return render_template('iframe.html')

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