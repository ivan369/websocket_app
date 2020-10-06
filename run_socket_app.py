
from app import my_flask_app, socketio

app = my_flask_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
