import eventlet
from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session
from datetime import timedelta
eventlet.monkey_patch(socket=True)

socketio = SocketIO()


def my_flask_app(debug=False):
    """Create an application."""
    app = Flask(
        __name__,
        static_url_path='/static/',
        static_folder='static/',
        template_folder='templates/'

    )

    app.debug = debug
    app.config['SECRET_KEY'] = 'secret!3339'
    app.config['SESSION_TYPE'] = 'filesystem'
    # The maximum number of items the session stores
    # before it starts deleting some, default 500
    app.config['SESSION_FILE_THRESHOLD'] = 300
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    Session(app)
    socketio.init_app(
        app,
        cors_allowed_origins=[],
        manage_session=False,
        async_mode='eventlet',
    )
    return app

