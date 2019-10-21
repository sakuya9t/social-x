from constant import ROOT_DIR
from similarity import TextUtils
from utils import Decryptor

config_template_path = ROOT_DIR + 'config/config-template.json'
config_deploy_template_path = ROOT_DIR + 'config/config-deploy-template.json'
Decryptor.generate_key()
TextUtils.initialize()

