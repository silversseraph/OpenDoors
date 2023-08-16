from threading import Lock
from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, emit
import requests
from  pywiegand import WiegandReader

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# Wiegand data0 = GPIO 6 / Raspi Pin 31, data1 = GPIO 5 / Raspi Pin 29
wr = WiegandReader(6, 5)

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(3)
        # reading keys
        card = wr.read()
        if card:
            socketio.emit('my_response', {'data': ''.join(card)})

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)

# Route for admin page
@app.route('/admin')
def admin():
    return render_template('table.html')  # render a template

# Receive the test request from client and send back a test response
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('test_response', {'data': 'Test response sent'})

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

# start the server with the 'run()' method
if __name__ == '__main__':
    socketio.run(app)
    # app.run(debug=True)

