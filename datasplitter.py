from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from time import gmtime, strftime
from imutils import paths
from time import time
from PIL import Image
import numpy as np
import argparse
import pathlib
import logging
import pickle
import os

# Usage: python datasplitter.py -d data_transfer

# Manual Settings (For every new version, increment the postfix!)
file_postfix = "-v1"
lb_pickle_name = "labels" + file_postfix + ".pickle"
root_dir = "train-data" + file_postfix + "/"
tmp_data_dir = "train/"
tmp_val_dir = "val/"
img_size=224

# Configure general logging
current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
log_name = 'T-LOG_' + current_time + '.log'
logging.basicConfig(filename=log_name,level=logging.DEBUG)
logging.info("SPLITTING SCRIPT")

ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",type=str, required=True,help="(required) the train data directory")
args = vars(ap.parse_args())

# initialize the data and labels
data, labels, data_test, labels_test, tmp_data, tmp_labels = ([] for i in range(6))

# grab the image paths and prepare them for splitting
print("[INFO] loading images...")
logging.info("[INFO] loading images...")
image_paths = sorted(list(paths.list_images(args["dataset"])))

file_count = sum(len(files) for _, _, files in os.walk(args["dataset"]))
logging.info("Total number of files: " + str(file_count))

counter = 0
numFiles = 100 # Just a random big number to be initialized with :)
for image_path in image_paths:
    label = image_path.split(os.path.sep)[-2]
    counter += 1
    
    # Once done with a subfolder, split content by designated amount
    if counter == numFiles:
        (trainX, testX, trainY, testY) = train_test_split(tmp_data, tmp_labels, test_size=0.2)
        labels.extend(trainY)
        labels_test.extend(testY)
        data.extend(trainX)
        data_test.extend(testX)

        # Reset
        counter = 0
        tmp_labels = []
        tmp_data = []
    else:
        files = os.listdir(args["dataset"]+"/"+label)
        numFiles = len(files)

    tmp_labels.append(label)
    current_img = Image.open(image_path)
    current_img = current_img.convert('RGB')
    current_img = current_img.resize((img_size, img_size), Image.ANTIALIAS)
    tmp_data.append(current_img)

# For last subdirectory
if len(tmp_data) > 0:
    (trainX, testX, trainY, testY) = train_test_split(tmp_data, tmp_labels, test_size=0.2)
    labels.extend(trainY)
    labels_test.extend(testY)
    data.extend(trainX)
    data_test.extend(testX)

print("Data length: " + str(len(data)))
print("Val Data length: " + str(len(data_test)))
logging.info("Data length: " + str(len(data)))
logging.info("Val Data length: " + str(len(data_test)))

# Create temporary data folder
counter = 0
print("[INFO]: Creating tmp data...")
for idx, img in enumerate(data):
    counter += 1
    name = (labels[idx] + str(counter) + ".jpg")
    out_path = root_dir + tmp_data_dir + labels[idx]
    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True) 
    img.save(out_path + "/" + name)

# Create temporary validation folder
counter = 0
print("[INFO]: Creating tmp validation data...")
for idx, img in enumerate(data_test):
    counter += 1
    name = (labels_test[idx] + str(counter) + ".jpg")
    out_path = root_dir + tmp_val_dir + labels_test[idx]
    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True) 
    img.save(out_path + "/" + name)

# binarize the labels
labels = np.array(labels)
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

# save the label binarizer to disk
print("[INFO] serializing label binarizer...")
with open(lb_pickle_name, "wb") as f:
    f.write(pickle.dumps(lb))

lb = pickle.loads(open(lb_pickle_name, "rb").read())
num_classes = len(lb.classes_)
logging.info("Number of classes: " + str(num_classes))
for cl in lb.classes_:
        logging.info("Classes: " + cl)
