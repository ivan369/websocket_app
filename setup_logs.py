import os
import logging
from logging.handlers import TimedRotatingFileHandler

root = os.path.dirname(os.path.abspath(__file__))
master_log_path = os.path.join(root, 'logs')
master_data_debug = os.path.abspath(os.path.join(master_log_path, "debug.log"))
master_data_info = os.path.abspath(os.path.join(master_log_path, "info.log"))
master_data_error = os.path.abspath(os.path.join(master_log_path, "error.log"))
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("application")

logger.setLevel(logging.DEBUG)
logger.propagate = False

sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)

sh.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s CONSOLE %(message)s'))
logger.addHandler(sh)

if not os.path.exists(master_log_path):
    os.mkdir(master_log_path)

# INFO LOGGER
fh_info = TimedRotatingFileHandler(master_data_info, backupCount=5)
fh_info.setLevel(logging.INFO)
fh_info.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s  %(message)s'))
logger.addHandler(fh_info)

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# ERROR LOGGER
fh_error = TimedRotatingFileHandler(master_data_error, backupCount=5)
fh_error.setLevel(logging.ERROR)
fh_error.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
logger.addHandler(fh_error)

# DEBUG LOGGER
fh_debug = TimedRotatingFileHandler(master_data_debug, backupCount=5)
fh_debug.setLevel(logging.DEBUG)
fh_debug.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s  %(message)s'))
logger.addHandler(fh_debug)
