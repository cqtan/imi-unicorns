from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.callbacks import TensorBoard,ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing import image
from time import gmtime, strftime
from keras.models import Model
from keras import optimizers 
from helpers import Plotter 
from imutils import paths
from time import time
from PIL import Image
from cnn import VGG16
import numpy as np
import argparse
import pathlib
import logging
import pickle
import os

# This script uses the VGG in the "cnn" directory. If you want to use the VGG from Keras, 
# use the script "imagenet_transfer.py"

# Usage: python train.py -t train-data/train -v train-data/val -l labels.pickle

# Manual Settings (For every new version, increment the postfix!)
file_postfix = "v1"
model_filepath = "model-" + file_postfix + ".h5"
epoch_amount = 50

#################################################################################################################################
#################################################################################################################################
# Following steps are required to fine-tune the model
#
#  1. Specify the path to training and testing data, along with number of classes and image size.
#  2. Do some random image transformations to increase the number of training samples and load the training and testing data
#  3. Create VGG16 network graph(without top) and load imageNet pre-trained weights
#  4. Add the top based on number of classes we have to the network created in step-3
#  5. Specify the optimizer, loss etc and start the training
##################################################################################################################################
##################################################################################################################################

# Configure general logging
current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
log_name = 'T-LOG_' + current_time + '.log'
logging.basicConfig(filename=log_name,level=logging.DEBUG)
logging.info("TRAINING SCRIPT")

##### Step-1:
############ Specify path to training and testing data. Minimum 100 images per class recommended.
############ Default image size is 160    
img_size=224
ap = argparse.ArgumentParser()
ap.add_argument("-t","--train_dir",type=str, required=True,help="(required) the train data directory")
ap.add_argument("-v","--val_dir",type=str, required=True,help="(required) the validation data directory")
ap.add_argument("-l","--label",type=str, required=True,help="(required) the label binarizer")
args = vars(ap.parse_args())

lb = pickle.loads(open(args["label"], "rb").read())
num_classes = len(lb.classes_)
logging.info("Number of classes: " + str(num_classes))
for cl in lb.classes_:
        logging.info("Classes: " + cl)

##### Step-2:
############ Do some random image transformations to increase the number of training samples
############ Note that we are scaling the image to make all the values between 0 and 1. That's how our pretrained weights have been done too
############ Default batch size is 8 but you can reduce/increase it depending on how powerful your machine is. 

batch_size=32

train_datagen = image.ImageDataGenerator(
        rotation_range=25,
        width_shift_range=0.1,
        height_shift_range=0.1,
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = image.ImageDataGenerator(rescale=1. / 255)
train_generator = train_datagen.flow_from_directory(
        args["train_dir"],
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        args["val_dir"],
        target_size=(img_size,img_size),
        batch_size=batch_size,
        class_mode='categorical')

##### Step-3:
############ Create VGG-16 network graph without the last layers and load imagenet pretrained weights
############ Default image size is 160    
print('loading the model and the pre-trained weights...')
base_model = VGG16.VGG16(include_top=False, weights='imagenet')

## Here we will print the layers in the network
i=0
for layer in base_model.layers:
    layer.trainable = False
    i = i+1
    print(i,layer.name)

##### Step-4:
############ Add the top as per number of classes in our dataset
############ Note that we are using Dropout layer with value of 0.2, i.e. we are discarding 20% weights
############
x = base_model.output
x = Dense(128)(x)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
predictions = Dense(num_classes, activation='softmax')(x)

##### Step-5:
############ Specify the complete model input and output, optimizer and loss
start_time = time()
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
checkpoint = ModelCheckpoint(model_filepath, monitor='val_loss', verbose=1,save_best_only=True,save_weights_only=False, mode='min',period=1)
callbacks_list = [checkpoint, tensorboard]

model = Model(inputs=base_model.input, outputs=predictions)
#model.compile(loss="categorical_crossentropy", optimizer=optimizers.SGD(lr=0.001, momentum=0.9),metrics=["accuracy"])
model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adam(),metrics=["accuracy"])
#model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adagrad(lr=0.01, epsilon=1e-08, decay=0.0),metrics=["accuracy"])

history = model.fit_generator(
        train_generator,
        steps_per_epoch=2*train_generator.samples/train_generator.batch_size,
        epochs=epoch_amount,
        validation_data = validation_generator,
        validation_steps=validation_generator.samples/validation_generator.batch_size,
        callbacks = callbacks_list
        )

plotter = Plotter.TrainPlotter(history, epoch_amount, file_postfix)
plotter.PlotLossAndAcc()

run_duration = (time() - start_time) / 60
end_msg = "Done! Run Duration:  " + str(run_duration) + " minutes."
print(end_msg)
logging.info(end_msg)
