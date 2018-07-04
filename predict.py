from cnn import VGG16
from keras.preprocessing import image
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from time import gmtime, strftime
from imutils import paths
import numpy as np
import argparse
import logging
import pickle
import os

# Configure general logging
current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
log_name = 'P-LOG_' + current_time + '.log'
logging.basicConfig(filename=log_name,level=logging.DEBUG)
logging.info("PREDICTION SCRIPT")

ap = argparse.ArgumentParser()
ap.add_argument("-m","--model",type=str, required=True,help="(required) the model")
ap.add_argument("-l","--labelbin",type=str, required=True,help="(required) the label binarizer file")
ap.add_argument("-d","--dataset",type=str, required=True,help="(required) the SBB data directory")
args = vars(ap.parse_args())

# Load the labels
lb = pickle.loads(open(args["labelbin"], "rb").read())
num_classes = len(lb.classes_)
logging.info("Number of classes: " + str(num_classes))
for cl in lb.classes_:
        logging.info("Classes: " + cl)

# Create the VGG model with own weights
base_model = VGG16.VGG16(include_top=False, weights=None)
x = base_model.output
x = Dense(128)(x)
x = GlobalAveragePooling2D()(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.load_weights(args["model"])

# Predict
image_paths = sorted(list(paths.list_images(args["dataset"])))
file_count = sum(len(files) for _, _, files in os.walk(args["dataset"]))
logging.info("Total number of files: " + str(file_count))

inputShape = (224,224) # Assumes 3 channel image
for image_path in image_paths:
    label = image_path.split(os.path.sep)[-2]
    image = load_img(image_path, target_size=inputShape)
    image = img_to_array(image)   # shape is (224,224,3)
    image = np.expand_dims(image, axis=0)  # Now shape is (1,224,224,3)
    image = image/255.0

    predictions = model.predict(image)
    print(predictions)

    idx = np.argmax(predictions)
    label = lb.classes_[idx]
    print(label)
