from flask import Blueprint, render_template

@app.route('/')
def home():
    return render_template('leftMenu.html')

@socketio.on('send_data')
def handle_data(data):
    emit('receive_data', {'result': "result"})
