from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('json')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('connect', namespace='/chess')
def connect(sid):
    print('Connection success', sid)
    emit("The message", namespace='/chess')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
