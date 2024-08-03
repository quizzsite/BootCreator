from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_caching import Cache
from celery import Celery, Task, shared_task

from config import Config
from .models import *
from .ext import *
from .routes import main
from .handlers import *

#App
app = Flask(__name__)
app.config.from_object(Config)

celery_init_app(app)
db.init_app(app)
appServer.init_app(app)
cors.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)

updateProjects(appServer)

def runServ():
    appServer.run(app, debug=True)

if __name__ == "__main__":
    runServ()