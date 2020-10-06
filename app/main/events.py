from flask_socketio import emit
from .routes import get_all_users, socekt_io_server_set_data_to_redis, ErrorMessageHandler
from .. import socketio
from setup_logs import logger


@socketio.on('connect', namespace='/socket_app')
def connect():
    """Sent by clients when they connect.
    A list of all users with favorite numbers is broadcast to all connected client..."""
    users = get_all_users()
    emit('status', {'msg': str(users)}, broadcast=True)


@socketio.on('disconnect', namespace='/socket_app')
def disconnect():
    emit('msg', 'User disconnected', broadcast=True)


@socketio.on('message', namespace='/socket_app')
def handle_message(data):
    """
    Sent by client, there is two type of message:
        1) "get_user_list" str(),
        2) user send username & favorite number,server save data into redis
    """
    try:
        if not isinstance(data, str):
            users = get_all_users()
            client_message = data['message']
            if client_message == "get_user_list":
                # return list of users
                emit('status', {'msg': str(users)}, broadcast=True)
            elif client_message == "create_user":
                # create user & favorite number
                username = data['username']
                favorite_number = data['favorite_number']

                status_result = socekt_io_server_set_data_to_redis(username, favorite_number)
                if status_result:
                    emit('status', {'msg': str(users)}, broadcast=True)

    except Exception as e:
        logger.error(ErrorMessageHandler.SOCKET_IO_SERVER_ERROR.value.format(e))


# Handles the default namespace
@socketio.on_error()
def error_handler(e):
    logger.error(ErrorMessageHandler.SOCKET_IO_SERVER_NAMESPACE_ERROR.value.format(e))


# handles the '/socket_app' namespace
@socketio.on_error('/socket_app')
def error_handler_chat(e):
    logger.error(ErrorMessageHandler.SOCKET_IO_SERVER_SPECIFIC_NAMESPACE_ERROR.value.format('socket_app', e))


# handles all namespaces without an explicit error handler
@socketio.on_error_default
def default_error_handler(e):
    logger.error(ErrorMessageHandler.SOCKET_IO_SERVER_NAMESPACE_ERROR.value.format(e))


@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()
