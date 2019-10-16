import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')
DRIVER_PATH = os.path.join(ROOT_DIR, 'chromedriver')
ALGOCONFIG_PATH = os.path.join(ROOT_DIR, 'config/algomodule.config')
DEPLOY_CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config-deploy.json')
KEY_FOLDER_PATH = os.path.join(ROOT_DIR, 'resources/')
REALTIME_MODE = 0
BATCH_MODE = 1

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

DATABASE_FEEDBACK = 'feedback'
DATABASE_CREDENTIAL = 'credential'
DATABASE_LABELED_DATA = 'similarity'
DATABASE_DATA_AWAIT_FEEDBACK = 'query_to_process'

MODEL_FILE_BASE_PATH = os.path.join(ROOT_DIR, 'model/')
