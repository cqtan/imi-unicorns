from cnn import VGG16
from helpers import ImageWriter, JsonBuilder
from keras.preprocessing import image
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from time import gmtime, strftime
from imutils import paths
from time import time
import numpy as np
import argparse
import logging
import pickle
import os

# Usage:
# python predict.py -m model-sbb3.h5 -l lb-sbb3.pickle -d data 

output_path = "out"

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
my_classes = lb.classes_
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

# ImageWriter.CreateScaffold(output_path, lb.classes_)
start_time = time()

json_builder = JsonBuilder.JsonBuilder(lb.classes_, 0.90)

img_counter = 0
inputShape = (224,224) # Assumes 3 channel image
for image_path in image_paths:
    image = load_img(image_path, target_size=inputShape)
    copy = image.copy()
    image = img_to_array(image)   # shape is (224,224,3)
    image = np.expand_dims(image, axis=0)  # Now shape is (1,224,224,3)
    image = image/255.0

    predictions = model.predict(image)
    #print(predictions)

    idx = np.argmax(predictions)
    label = lb.classes_[idx]
    highest_pred = predictions.max()

    #print(label + ": " + str(highest_pred))

    # ImageWriter.WriteImage(copy, output_path, image_path, label, highest_pred)
    json_builder.AppendImageData(image_path, predictions)
    img_counter += 1
    print(str(img_counter) + " / " + str(file_count) + " done...")

json_builder.CreateJson()

run_duration = (time() - start_time) / 60
end_msg = "Done! Run Duration:  " + str(run_duration) + " minutes."
print(end_msg)
logging.info(end_msg)
