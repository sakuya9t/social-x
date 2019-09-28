import os
import ast

from constant import CONFIG_PATH
from similarity.Config import Config
from utils import logger
from utils.InsUtils import InsUtilsNoLogin
from utils.TwiUtils import TwiUtilsNoLogin

CONFIG = Config(CONFIG_PATH)
PAIRING_FILE_PATH = CONFIG.get("sampler/pairing_file")
INSTA_FOLDER = CONFIG.get("sampler/instagram_folder")
TWITTER_FOLDER = CONFIG.get("sampler/twitter_folder")

"""
Function:
    Automatically go through pairing file, download instagram and twitter data and save to file.
Drawback:
    The issue of selenium, browser not normally closed when closing instances. Have to restart 
    service every couple days, while killing all chromedriver/chrome processes.
"""

items = []
with open(PAIRING_FILE_PATH, "r") as file:
    while True:
        line = file.readline()
        if not line:
            break
        items.append(ast.literal_eval(line))

twitter_accounts = [x['twitter'] for x in items]
insta_accounts = [x['instagram'] for x in items]

for i in range(len(items)):
    try:
        twi_account = twitter_accounts[i]
        ins_account = insta_accounts[i]
        twi_filename = INSTA_FOLDER + ins_account + '.txt'
        ins_filename = TWITTER_FOLDER + twi_account + '.txt'
        if os.path.exists(twi_filename):
            continue
        if os.path.exists(ins_filename):
            continue
        logger.info('{} / {} complete, insta account {}, twitter account {}.'.format(i, len(items), twi_account, ins_account))
        insta = InsUtilsNoLogin(False)
        twi = TwiUtilsNoLogin(False)
        logger.info('Start parsing Instagram...')
        ins_info = insta.parse(ins_account)
        insta.close()
        if ins_info == "INVALID":
            logger.warning('Invalid Instagram account.')
            continue
        logger.info('Start parsing Twitter...')
        twi_info = twi.parse(twi_account)
        twi.close()
        if len(twi_info.keys()) == 0:
            logger.warning('Invalid Twitter account.')
            continue
        with open('/data/dev/insdata/'+ins_account+'.txt', "a") as file:
            file.write(str(ins_info))
        with open('/data/dev/twidata/'+twi_account+'.txt', "a") as file:
            file.write(str(twi_info))
    except Exception as e:
        logger.error(e)
        continue
