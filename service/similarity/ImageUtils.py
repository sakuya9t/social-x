import json
import os
from io import BytesIO

import requests
from PIL import Image
from google.cloud import vision
from sklearn.metrics.pairwise import cosine_similarity

from similarity.img_to_vec import Img2Vec
from similarity.Config import Config
from constant import CONFIG_PATH


class MSFaceService:
    def __init__(self):
        subscription_key = Config(CONFIG_PATH).get('microsoft/subscription_key')
        self.headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    def detect_face(self, image_url):
        api_url = 'https://australiaeast.api.cognitive.microsoft.com/face/v1.0/detect'
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,'
                                    'accessories,blur,exposure,noise',
        }
        response = requests.post(api_url, params=params, headers=self.headers, json={"url": image_url})
        return response.json()

    def face_similarity(self, url1, url2):
        api_url = 'https://australiaeast.api.cognitive.microsoft.com/face/v1.0/verify'
        faceId1 = self.detect_face(url1)[0]['faceId']
        faceId2 = self.detect_face(url2)[0]['faceId']
        body = {
            'faceId1' : faceId1,
            'faceId2' : faceId2
        }
        response = requests.post(api_url, headers=self.headers, json=body)
        return json.dumps(response.json())


class GoogleVisionUtils:
    def __init__(self):
        keyfile = Config(CONFIG_PATH).get('google/keyfile_path')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile

    def detect_labels(self, uri):
        """Detects labels in the file located in Google Cloud Storage or on the
        Web."""
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.label_detection(image=image)
        labels = response.label_annotations
        labels = [x.description for x in labels]

        return labels


def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def webimage_similarity(url1, url2):
    img1 = load_image(url1)
    img2 = load_image(url2)
    
    img2vec = Img2Vec(model='alexnet')
    vec1 = img2vec.get_vec(img1)
    img2vec = Img2Vec(model='alexnet')
    vec2 = img2vec.get_vec(img2)
    res = {'alexnet': cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]}
    
    img2vec = Img2Vec()
    vec1 = img2vec.get_vec(img1)
    img2vec = Img2Vec()
    vec2 = img2vec.get_vec(img2)
    res['resnet18'] = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
    return res


if __name__ == '__main__':
    service = GoogleVisionUtils()
    print(service.detect_labels('https://pbs.twimg.com/media/EDc7zqhU8AAnyVN?format=jpg&name=medium'))
