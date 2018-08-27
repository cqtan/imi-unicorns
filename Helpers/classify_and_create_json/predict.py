from cnn import VGG16
from keras.applications import vgg16
from helpers import ImageWriter, JsonBuilder
from keras.preprocessing import image
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from time import gmtime, strftime
from imutils import paths
from time import time
from PIL import Image
from keras import models, layers
import numpy as np
import argparse
import logging
import pickle
import os

# Usage:
# python predict.py -m model.h5 -l label.pickle -d data
# NOTE: Prediction might take a while! On GTX 980ti about 2 hours for 200k jpg images.

image_size = 224
write_images = False

if write_images == True: 
    image_writer_out_path = "out" # For helpers/ImageWriter.py 

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

##### Step 1: Load VGG from Keras without top and no weights.
vgg_model = vgg16.VGG16(weights=None, include_top=False, input_shape=(image_size, image_size, 3))
model = models.Sequential()
model.add(vgg_model)

# Add new top layers
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='softmax'))

# or use a different top layers, such as these but make sure trained weights have identical topology!:
""" model.add(layers.Flatten())
model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='softmax')) """

# Load weights to the new VGG model
model.load_weights(args["model"])

##### Step 2: Predict
image_paths = sorted(list(paths.list_images(args["dataset"])))
file_count = sum(len(files) for _, _, files in os.walk(args["dataset"]))
logging.info("Total number of files: " + str(file_count))
start_time = time()

if write_images == True: 
    ImageWriter.CreateScaffold(image_writer_out_path, lb.classes_)

# Initialize JsonBuilder with list of class names and accuracy threshold.
json_builder = JsonBuilder.JsonBuilder(lb.classes_, 0.90)

img_counter = 0
inputShape = (224,224) # Assumes 3 channel image
for image_path in image_paths:
    image = load_img(image_path)
    if write_images == True: 
        copy = image.copy()
    image = image.resize(inputShape, Image.ANTIALIAS)
    image = img_to_array(image)   # shape is (224,224,3)
    image = np.expand_dims(image, axis=0)  # Now shape is (1,224,224,3)
    image = image/255.0

    predictions = model.predict(image)

    # Get prediction with highest accuracy
    idx = np.argmax(predictions)
    label = lb.classes_[idx]
    highest_pred = predictions.max()

    #print(label + ": " + str(highest_pred))
    if write_images == True: 
        ImageWriter.WriteImage(copy, image_writer_out_path, image_path, label, highest_pred)
    json_builder.AppendImageData(image_path, predictions)
    img_counter += 1
    print(str(img_counter) + " / " + str(file_count) + " done...")

json_builder.CreateJson()

run_duration = (time() - start_time) / 60
end_msg = "Done! Run Duration:  " + str(run_duration) + " minutes."
print(end_msg)
logging.info(end_msg)
