import os
import ast

import sys
parent_path = os.path.abspath('.')
sys.path.append(parent_path)

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
    twi = None
    insta = None
    try:
        twi_account = twitter_accounts[i]
        ins_account = insta_accounts[i]
        twi_filename = INSTA_FOLDER + ins_account + '.txt'
        ins_filename = TWITTER_FOLDER + twi_account + '.txt'
        if os.path.exists(twi_filename):
            continue
        if os.path.exists(ins_filename):
            continue
        logger.info('{} / {} complete, twitter account {}, instagram account {}.'.format(i, len(items), twi_account, ins_account))
        insta = InsUtilsNoLogin(False)
        twi = TwiUtilsNoLogin(False)
        if insta.is_invalid(ins_account):
            logger.warning('Invalid Instagram account.')
            insta.close()
            twi.close()
            continue
        if twi.isSuspendedOrInvalid(twi_account):
            logger.warning('Invalid Twitter account.')
            insta.close()
            twi.close()
            continue
        logger.info('Start parsing Instagram...')
        ins_info = insta.parse(ins_account)
        insta.close()
        logger.info('Start parsing Twitter...')
        twi_info = twi.parse(twi_account)
        twi.close()
        with open('/data/dev/insdata/'+ins_account+'.txt', "a") as file:
            file.write(str(ins_info))
        with open('/data/dev/twidata/'+twi_account+'.txt', "a") as file:
            file.write(str(twi_info))
    except Exception as e:
        logger.error(e)
        if twi:
            twi.close()
        if insta:
            insta.close()
        continue
