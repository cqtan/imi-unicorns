from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.applications import resnet50
from collections import OrderedDict    
from time import gmtime, strftime
from helpers import JsonBuilder
import matplotlib.pyplot as plt
from imutils import paths
from time import time
import numpy as np
import argparse
import logging
import pickle
import keras
import json
import os

# Usage:
# python predict-imagenet.py -d data
class ImageClassifier:
    def __init__(self, data_path):
        self.resnet_model = resnet50.ResNet50(weights='imagenet')
        self.data_path = data_path
        self.labels_for_counting = {}
        self.labels = ['vase', 'church', 'suspension_bridge', 'pedestal', 'swing', 'castle', 'airship', 'pickelhaube', 'military_uniform', 'prayer_rug', 'rule', 'doormat', 'envelope', 'fountain', 'book_jacket', 'crossword_puzzle', 'slide_rule']
        self.inputShape = (224,224) # Assumes 3 channel image
        self.output_filename = "imagenet_counts.json"

    def predict(self):
        file_count = sum(len(files) for _, _, files in os.walk(self.data_path))
        logging.info("Total number of files: " + str(file_count))
        img_counter = 0
        image_paths = sorted(list(paths.list_images(self.data_path)))

        json_builder = JsonBuilder.JsonBuilder(self.labels, 0.75)

        for image_path in image_paths:
            image = load_img(image_path, target_size=self.inputShape)
            image = img_to_array(image)   # shape is (224,224,3)
            image = np.expand_dims(image, axis=0)  # Now shape is (1,224,224,3)
            processed_image = resnet50.preprocess_input(image.copy())
            predictions = self.resnet_model.predict(processed_image)

            # convert the probabilities to class labels
            # If you want to see the top 3 predictions, specify it using the top argument
            label_resnet = decode_predictions(predictions)
            _, label, acc = label_resnet[0][0]
            #self.appendCountsOnly(label, acc, 0.75)
            if label in self.labels:
                json_builder.AppendImageDataDecoded(image_path, label, acc)

            img_counter += 1
            print(str(img_counter) + " / " + str(file_count) + " done...")
        
        json_builder.CreateJson()

    def appendCountsOnly(self, label, accuracy, threshold):
        if accuracy > threshold:
            if label in self.labels_for_counting:
                self.labels_for_counting[label] += 1
            else:
                self.labels_for_counting[label] = 1

    def writeLabels(self):
        ordered_dict = OrderedDict(sorted(self.labels_for_counting.items(), key=lambda t: t[1]))

        with open(self.output_filename, 'w') as json_file:
            json.dump(ordered_dict, json_file, indent=4)
        print("Created " + self.output_filename)

if __name__ == '__main__':
    filename = 'images/cat.jpg'

    # Configure general logging
    current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    log_name = 'P-ImageNet-LOG_' + current_time + '.log'
    logging.basicConfig(filename=log_name,level=logging.DEBUG)
    logging.info("PREDICTION SCRIPT")

    ap = argparse.ArgumentParser()
    ap.add_argument("-d","--dataset",type=str, required=True,help="(required) the SBB data directory")
    args = vars(ap.parse_args())

    start_time = time()

    ic = ImageClassifier(args["dataset"])
    ic.predict()
    #ic.writeLabels()

    run_duration = (time() - start_time) / 60
    end_msg = "Done! Run Duration:  " + str(run_duration) + " minutes."
    print(end_msg)
    logging.info(end_msg)
