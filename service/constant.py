import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')
DRIVER_PATH = os.path.join(ROOT_DIR, 'chromedriver')
ALGOCONFIG_PATH = os.path.join(ROOT_DIR, 'config/algomodule.config')
DEPLOY_CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config-deploy.json')
REALTIME_MODE = 0
BATCH_MODE = 1

DATABASE_FEEDBACK = 'feedback'
DATABASE_CREDENTIAL = 'credential'
DATABASE_LABELED_DATA = 'similarity'
DATABASE_DATA_AWAIT_FEEDBACK = 'query_to_process'
