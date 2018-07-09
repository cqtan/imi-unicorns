import json
import numpy as np
import os
import math

class JsonBuilder:

    def __init__(self, labels, threshold):
        self.output_filename = "categories-18.json"
        self.output_filename_alt = "categories_alt-18.json"
        self.labels = labels
        self.threshold = threshold
        self.master_dict = {
            "category_data": {},
            "book_data": {},
            "image_data": []
        }
        self.alt_dict = {
            "category_data": {},
            "book_data": {},
            "image_data": []
        }
        self.InitializeCategoryData()

    def CreateJson(self):
        self.AppendCategoryData()
        with open(self.output_filename, 'w') as json_file:
            json.dump(self.master_dict, json_file, indent=4)
        print("Created " + self.output_filename)

        with open(self.output_filename_alt, 'w') as json_file:
            json.dump(self.alt_dict, json_file, indent=4)
        print("Created " + self.output_filename_alt)
        

    def AppendImageData(self, image_path, predictions):
        features = self.GetFeatures(predictions)
        features_with_acc = self.GetFeaturesWithAcc(predictions)
        path = self.BuildCustomPath(image_path)
        ppn = image_path.split(os.path.sep)[-2]

        self.AppendBookData(ppn, features)
        self.UpdateCategoryData(ppn, features)

        image_dict = {}
        image_dict['features'] = features
        image_dict['path'] = path
        image_dict['ppn'] = ppn

        image_dict_acc = {}
        image_dict_acc['features'] = features_with_acc
        image_dict_acc['path'] = path
        image_dict_acc['ppn'] = ppn

        self.master_dict['image_data'].append(image_dict)
        self.alt_dict['image_data'].append(image_dict_acc)

    def AppendImageDataDecoded(self, image_path, label, acc):
        if acc > self.threshold:
            highest_pred = math.floor(acc * 100)
            features = [label]
            features_with_acc = {label: highest_pred}
            path = self.BuildCustomPath(image_path)
            ppn = image_path.split(os.path.sep)[-2]

            self.AppendBookData(ppn, features)
            self.UpdateCategoryData(ppn, features)

            image_dict = {}
            image_dict['features'] = features
            image_dict['path'] = path
            image_dict['ppn'] = ppn

            image_dict_acc = {}
            image_dict_acc['features'] = features_with_acc
            image_dict_acc['path'] = path
            image_dict_acc['ppn'] = ppn

            self.master_dict['image_data'].append(image_dict)
            self.alt_dict['image_data'].append(image_dict_acc)

    def AppendBookData(self, ppn, features):
        if ppn not in self.master_dict["book_data"]:
            self.master_dict["book_data"][ppn] = []

        for feature in features:
            if feature not in self.master_dict["book_data"][ppn]:
                self.master_dict["book_data"][ppn].append(feature)

        if ppn not in self.alt_dict["book_data"]:
            self.alt_dict["book_data"][ppn] = []

        for feature in features:
            if feature not in self.alt_dict["book_data"][ppn]:
                self.alt_dict["book_data"][ppn].append({feature: 1})
            else:
                self.alt_dict["book_data"][ppn][feature] += 1  
        
    def AppendCategoryData(self):
        for label in self.labels:
            title = self.ConvertToTitle(label)
            self.master_dict['category_data'][title] = label

    def InitializeCategoryData(self):
        for label in self.labels:
            title = self.ConvertToTitle(label)
            self.alt_dict['category_data'][title] = []
            self.alt_dict['category_data'][title].append({label: 0})

    def UpdateCategoryData(self, ppn, features):
        for feature in features:
            title = self.ConvertToTitle(feature)
            #if feature in self.alt_dict["category_data"][title]:
            #    self.alt_dict['category_data'][title][feature] += 1
            if any(feature in x for x in self.alt_dict['category_data'][title]):
                self.alt_dict['category_data'][title][feature] += 1


    def GetFeatures(self, predictions):
        features = []
        pred_list = predictions.tolist()

        for preds in pred_list:
            for pred in preds:
                if pred > self.threshold:
                    idx = np.argmax(predictions)
                    features.append(self.labels[idx])
        return features

    def GetFeaturesWithAcc(self, predictions):
        features = {}
        pred_list = predictions.tolist()
        highest_pred = math.floor(predictions.max() * 100)

        for preds in pred_list:
            for pred in preds:
                if pred > self.threshold:
                    idx = np.argmax(predictions)
                    features[self.labels[idx]] = highest_pred
        return features        

    def BuildCustomPath(self, image_path):
        custom_path = "dist/ChasingUnicornsAndVampires/assets/images"
        ppn = image_path.split(os.path.sep)[-2]
        filename = image_path.split(os.path.sep)[-1]
        filename = filename[:-3]
        #path = os.path.join(custom_path, ppn, filename) + 'jpg'
        path = custom_path + "/" + ppn + "/" + filename + "jpg"
        return path

    def ConvertToTitle(self, label):
        if label.find("_") > 0:
            label.replace("_", " ")
        return label.title()

        


        
