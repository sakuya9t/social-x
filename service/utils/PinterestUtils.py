from bs4 import BeautifulSoup
import requests
from multiprocessing.dummy import Pool as ThreadPool
import json

from utils.AbstractParser import AbstractParser

base_pin_url = 'https://www.pinterest.com/pin/'
THREAD_POOL_SIZE = 20


def get_pin_annotation(pin):
    try:
        url = pin['url']
        resp = requests.get(url)
        data = resp.text
        soup = BeautifulSoup(data)
        info = json.loads(soup.find("script", {"id": "initial-state"}).get_text())
        pin_info = list(filter(lambda x: x['name'] == 'PinResource', info['resourceResponses']))[0]['response']
        annotation = pin_info['data']['pin_join']['visual_annotation'] if pin_info['status'] == 'success' else []
        return annotation
    except:
        return []


def get_pin_annotation_parallel(pins):
    pool = ThreadPool(THREAD_POOL_SIZE)
    results = pool.map(get_pin_annotation, pins)
    return results


def parse_pinterest(username, profile_only=False):
    url = "https://www.pinterest.com/{}".format(username)
    resp = requests.get(url)
    data = resp.text
    soup = BeautifulSoup(data)

    info = json.loads(soup.find("script", {"id": "initial-state"}).get_text())
    info = list(info['resources']['data']['UnauthReactUserProfileResource'].values())[0]['data']
    # rename properties to match other platforms
    info['profile']['image'] = info['profile'].pop('image_xlarge_url')
    info['profile']['description'] = info['profile'].pop('about')
    boards = [(x['name'], x['pin_count']) for x in info['boards']]

    if profile_only:
        user_data = info['profile']
    else:
        pins = info['pins']
        pin_list = parse_pins(pins)
        user_data = {'profile': info['profile'], 'posts_content': pin_list, 'boards': boards}
    return user_data


def parse_pins(pins):
    pins = list(filter(lambda x: x['pin_join'] and x['pin_join']['annotations_with_links'], pins))
    pin_list = [{'labels': list(x['pin_join']['annotations_with_links'].keys()),
                 'url': base_pin_url + x['id'],
                 'id': x['id'],
                 'image': x['images']['orig']['url']} for x in pins]
    additional_labels = get_pin_annotation_parallel(pin_list)
    for i in range(len(pin_list)):
        pin_list[i]['labels'] += additional_labels[i]
        pin_list[i]['labels'] = list(dict.fromkeys(pin_list[i]['labels']))
    return pin_list


class PinterestUtils(AbstractParser):
    def parse(self, username):
        return parse_pinterest(username)

    def parse_profile(self, username):
        return parse_pinterest(username, profile_only=True)
