import json


class Config:
    def __init__(self, file_path):
        with open(file_path, 'r') as json_data_file:
            self.data = json.load(json_data_file)

    def get(self, attributes):
        att = attributes.split("/")
        curr = self.data
        for attribute in att:
            if attribute not in curr.keys():
                return None
            curr = curr[attribute]
        return curr
