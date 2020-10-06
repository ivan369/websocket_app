import json
from flask import render_template, request, jsonify

from . import main
from .redis_managment import RedisManagement
from setup_logs import logger
import functools
from flask_login import current_user
from flask_socketio import disconnect
from enum import Enum


class ErrorMessageHandler(Enum):

    SOCKET_IO_SERVER_ERROR = "Error occurred on socket-io server, while handling event message, error: {}"
    SOCKET_IO_SERVER_NAMESPACE_ERROR = "Error occurred on socket-io server, while handling namespace, error: {}"
    SOCKET_IO_SERVER_SPECIFIC_NAMESPACE_ERROR = "Error occurred on socket-io server, while handling namespace: {}, error: {}"

    GET_DATA_FROM_REDIS_ERROR = "Error occurred while retrieving data from redis error: {}"
    SET_DATA_TO_REDIS = "Error occurred while set data to redis, error: {}"

    USER_SET_DATA_TO_REDIS_USING_FLASK_SUCCESS = "User set data to redis successfully, POST request, data: {}"
    USER_SET_DATA_TO_REDIS_USING_SOCKET_IO_SUCCESS = "User set data to redis successfully, SOCKET-IO server, data: {}"


# render initial template
@main.route('/', methods=['GET', 'POST'])
def initial_template():
    """My initial template"""
    return render_template('index.html')


@main.route("/get_all_users")
def get_all_users():
    """
    Get all users from redis based on specific key...
    """
    response = []
    try:
        redis_data = get_data_form_redis()
        response = {"data": redis_data}
    except Exception as e:
        logger.error(ErrorMessageHandler.GET_DATA_FROM_REDIS_ERROR.value.format(e))
    return json.dumps(response)


@main.route("/set_data_to_redis", methods=['POST'])
def set_data_to_redis():
    """
    Set data to redis, using standard POST request,
    specific key (websocket_) & value (username & favorite number)
    """

    response = jsonify("success")

    try:
        username = request.form['username']
        favorite_number = request.form['favorite_number']
        redis_key = "websocket_"+str(username)
        redis_key = redis_key.strip()
        username = username.strip()
        favorite_number = favorite_number.strip()

        if not username:
            response = jsonify("Please define your username!")
        if not favorite_number:
            response = jsonify("Please define your favorite number!")

        redis_value = {
            'username': username,
            'favorite_number': favorite_number,
        }

        RedisManagement.hmset_to_redis(redis_key, redis_value)
        logger.info(ErrorMessageHandler.USER_SET_DATA_TO_REDIS_USING_FLASK_SUCCESS.value.format(redis_value))
    except Exception as e:
        logger.error(ErrorMessageHandler.SET_DATA_TO_REDIS.value.format(e))
    return response


@main.route("/redis_save")
def socekt_io_server_set_data_to_redis(username, favorite_number):
    """
    This method use socekt-io server to set user data to redis,
    specific key (websocket_) & value (username & favorite number)
    :param username: str(), username
    :param favorite_number: int(), favorite number
    :return: bool(), status
    """

    try:
        status = True
        username = username.strip()
        favorite_number = favorite_number.strip()
        redis_key = "websocket_"+str(username)
        redis_key = redis_key.strip()

        redis_value = {
            'username': username,
            'favorite_number': favorite_number,
        }
        logger.info(ErrorMessageHandler.USER_SET_DATA_TO_REDIS_USING_SOCKET_IO_SUCCESS.value.format(redis_value))
        RedisManagement.hmset_to_redis(redis_key, redis_value)
    except Exception as e:
        logger.error(ErrorMessageHandler.SET_DATA_TO_REDIS.value.format(e))

        status = False

    return status


@main.route("/get_data_form_redis")
def get_data_form_redis():
    all_users = []
    try:
        redis_data = RedisManagement.get_all_keys_from_redis()
        redis_data = list(filter(lambda x: x.startswith('websocket_'), redis_data))
        redis_data = sorted(redis_data)
        for key in redis_data:
            redis_data_for_key = RedisManagement.get_data_from_redis_hgetall(key)
            if redis_data_for_key not in all_users:
                all_users.append(
                    [redis_data_for_key['username'],
                     redis_data_for_key['favorite_number']]
                )
    except Exception as e:
        logger.error(ErrorMessageHandler.GET_DATA_FROM_REDIS_ERROR.value.format(e))
    return all_users


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped
