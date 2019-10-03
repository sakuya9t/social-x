import datetime

from constant import CONFIG_PATH
from similarity.Config import Config

INFO = 0
WARNING = 1
ERROR = 2

enable_color = Config(CONFIG_PATH).get('logger/color-enabled')
write_to_file = Config(CONFIG_PATH).get('logger/write-to-file')
log_file_path = Config(CONFIG_PATH).get('logger/logfile-path')


def info(message):
    __print_message(message, INFO)


def error(message):
    __print_message(message, ERROR)


def warning(message):
    __print_message(message, WARNING)


def __print_message(message, level):
    color = {INFO: '\033[0m', WARNING: '\033[93m ', ERROR: '\033[91m '}
    prefix = {INFO: '(INFO)', WARNING: '(WARNING)', ERROR: '(ERROR)'}
    time = str(datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"))
    log_body = '{prefix} {time} {message}'.format(prefix=prefix[level], time=time, message=message)
    if write_to_file:
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_body + '\n')
    elif enable_color:
        log_body = '{} {}'.format(color[level], log_body)
        print(log_body)
