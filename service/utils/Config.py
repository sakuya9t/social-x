import json


class Config:
    def __init__(self, file_path):
        with open(file_path, 'r') as json_data_file:
            self.data = json.load(json_data_file)

    def get(self, attribute):
        if attribute not in self.data.keys():
            return None
        return self.data[attribute]
