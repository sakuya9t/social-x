import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')
DRIVER_PATH = os.path.join(ROOT_DIR, 'chromedriver')
ALGOCONFIG_PATH = os.path.join(ROOT_DIR, 'config/algomodule.config')
DEPLOY_CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config-deploy.json')
REALTIME_MODE = 0
BATCH_MODE = 1

DATABASE_FEEDBACK = 'feedback'
DATABASE_QUERY_RESULT = 'score'
DATABASE_CREDENTIAL = 'credential'
DATABASE_LABELED_DATA = 'similarity'
DATABASE_DATA_AWAIT_BATCH = 'query_to_process'
DATABASE_DATA_AWAIT_FEEDBACK = 'auto_similarity'
