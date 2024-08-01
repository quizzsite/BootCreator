from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_caching import Cache
from config import Config

#App
app = Flask(__name__)
app.config.from_object(Config)
#Socketio
appServer = SocketIO(app)

#redis
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

#Security
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
@appServer.on('send_data')
def handle_data(data):
    emit('receive_data', {'result': "result"})

@app.route('/')
def home():
    return render_template('leftMenu.html')

@app.route('/editor')
def editor():
    return render_template('iframe.html')

def runServ():
    appServer.run(app, debug=True)

if __name__ == "__main__":
    runServ()