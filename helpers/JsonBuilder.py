import json
import numpy as np
import os


class JsonBuilder:
    def __init__(self, labels, threshold):
        self.labels = labels
        self.threshold = threshold
        self.master_dict = {
            "category_data": {},
            "book_data": {},
            "image_data": []
        }

    def CreateJson(self):
        with open('categories.json', 'w') as json_file:
            json.dump(self.master_dict, json_file, indent=4)

    def AppendImageData(self, image_path, predictions):
        features = self.GetFeatures(predictions)
        path = self.BuildCustomPath(image_path)
        ppn = image_path.split(os.path.sep)[-2]

        self.AppendBookData(ppn, features)

        image_dict = {}
        image_dict['features'] = features
        image_dict['path'] = path
        image_dict['ppn'] = ppn

        self.master_dict['image_data'].append(image_dict)

    def AppendBookData(self, ppn, features):
        if ppn not in self.master_dict["book_data"]:
            self.master_dict["book_data"][ppn] = []

        for feature in features:
            if feature not in self.master_dict["book_data"][ppn]:
                self.master_dict["book_data"][ppn].append(feature)
        

    def AppendCategoryData(self):
        pass

    def GetFeatures(self, predictions):
        features = []
        pred_list = predictions.tolist()
        for preds in pred_list:
            for pred in preds:
                if pred > self.threshold:
                    idx = np.argmax(predictions)
                    features.append(self.labels[idx])
        return features

    # dist/ChasingUnicornsAndVampires/assets/images/" + PPN + <imageName.ending>
    def BuildCustomPath(self, image_path):
        custom_path = "dist/ChasingUnicornsAndVampires/assets/images"
        ppn = image_path.split(os.path.sep)[-2]
        filename = image_path.split(os.path.sep)[-1]
        filename = filename[:-3]
        #path = os.path.join(custom_path, ppn, filename) + 'jpg'
        path = custom_path + "/" + ppn + "/" + filename + "jpg"
        return path

        


        
