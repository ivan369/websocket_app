import json
import redis
from os import environ
from dotenv import load_dotenv
from pathlib import Path
import os


# Get the base directory
basepath = Path()
basedir = str(basepath.cwd())
# Load the environment variables
envars = basepath.cwd() / '.env'
load_dotenv(envars)
# Read an environment variable.
REDIS_URL = os.getenv('REDIS_URL')
REDIS_PORT = os.getenv('REDIS_PORT')
print("EEEEEEEEEEEEEEE", REDIS_PORT, REDIS_URL)

conn = redis.Redis(host=REDIS_URL, port=REDIS_PORT, decode_responses=True)


def generate_json(json_obj):
    return json.dumps(json_obj, sort_keys=True)


def generate_hash_for_json(json_obj):
    import hashlib
    unicode_object = generate_json(json_obj)
    hsh = hashlib.sha256(str(unicode_object).encode('utf-8')).hexdigest()
    return hsh


class RedisManagement(object):
    @classmethod
    def compare_data(cls, key, data):
        if conn.get(key) is not None:
            old_data = conn.get(key)
            new_data = data

            hash_new_data = generate_hash_for_json(new_data)
            hash_old_data = generate_hash_for_json(json.loads(old_data))

            if str(hash_new_data) != str(hash_old_data):
                cls.set_data_to_redis(key, data)
                return True
            else:
                return True

        return False

    @classmethod
    def get_data_from_redis(cls, key):
        return conn.get(key)

    @classmethod
    def get_data_from_redis_hgetall(cls, key):
        return conn.hgetall(key)

    @classmethod
    def get_data_from_redis_key_start_with(cls, key):
        return conn.scan(match=key)

    @classmethod
    def set_data_to_redis(cls, key, data, redis_time_cache=20):
        conn.set(key, json.dumps(data), redis_time_cache)

    @classmethod
    def set_data_to_redis_permanent(cls, key, data):
        conn.set(key, json.dumps(data))

    @classmethod
    def hmset_to_redis(cls, key, data):
        conn.hmset(key, data)

    @classmethod
    def set_to_redis_expire(cls, key, time_in_seconds):
        conn.expire(key, time_in_seconds)

    @classmethod
    def redis_key_exist_check(cls, key):
        return conn.exists(key)

    @classmethod
    def get_all_keys_from_redis(cls):
        return conn.keys()

    @classmethod
    def set_or_get_redis_data(cls, key, data):
        status = cls.compare_data(key, data)
        if not status:
            cls.set_data_to_redis(key, data)
            return json.loads(cls.get_data_from_redis(key))
        else:
            return json.loads(cls.get_data_from_redis(key))
