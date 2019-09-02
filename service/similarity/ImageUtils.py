import requests
import json
import os
from google.cloud import vision
from PIL import Image
import requests
from io import BytesIO
from sklearn.metrics.pairwise import cosine_similarity
from similarity.img_to_vec import Img2Vec


class MSFaceService:
    subscription_key = "70fa1e3147b14bf5af726186bc7bbcc2"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    def detect_face(self, image_url):
        api_url = 'https://australiaeast.api.cognitive.microsoft.com/face/v1.0/detect'
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
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
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/data/dev/bright-benefit-250309-5fa89d250130.json"

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
