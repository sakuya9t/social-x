from bs4 import BeautifulSoup
import requests
from multiprocessing.dummy import Pool as ThreadPool
import json

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
    pool = ThreadPool(20)
    results = pool.map(get_pin_annotation, pins)
    return results

def parse_pinterest(username):
    url = "https://www.pinterest.com/{}".format(username)
    base_pin_url = 'https://www.pinterest.com/pin/'
    resp = requests.get(url)
    data = resp.text
    soup = BeautifulSoup(data)

    info = json.loads(soup.find("script", {"id": "initial-state"}).get_text())
    info = list(info['resources']['data']['UnauthReactUserProfileResource'].values())[0]['data']
    info['profile']['image'] = info['profile']['image_xlarge_url']

    pins = info['pins']
    pins = list(filter(lambda x: x['pin_join'] and x['pin_join']['annotations_with_links'], pins))
    pin_list = [{'labels': list(x['pin_join']['annotations_with_links'].keys()), 
                 'url': base_pin_url + x['id'],
                 'id': x['id'],
                 'image': x['images']['orig']['url']} for x in pins]
    additional_labels = get_pin_annotation_parallel(pin_list)
    for i in range(len(pin_list)):
        pin_list[i]['labels'] += additional_labels[i]
        pin_list[i]['labels'] = list(dict.fromkeys(pin_list[i]['labels']))
    boards = [(x['name'], x['pin_count']) for x in info['boards']]
    user_data = {'profile': info['profile'], 'posts_content': pin_list, 'boards': boards}
    return user_data
