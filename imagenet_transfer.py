from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras import layers, models, optimizers
from keras.preprocessing import image
from keras.applications import vgg16
from time import gmtime, strftime
from helpers import Plotter 
from imutils import paths
from time import time
from PIL import Image
import numpy as np
import argparse
import pathlib
import logging
import pickle
import os

# Usage: python imagenet_transfer.py -dt train-data-sbb5-transfer/train -dv train-data-sbb5-transfer/val -l lb-sbb5-transfer.pickle

epoch_amount = 100
image_size = 224
batch_size=24
model_name = 'sbb-vgg16_v6'
plot_file_name = 'vgg-plot_v6'

start_time = time()

# Configure general logging
current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
log_name = 'Transfer-LOG_' + current_time + '.log'
logging.basicConfig(filename=log_name,level=logging.DEBUG)
logging.info("TRAINING SCRIPT")

ap = argparse.ArgumentParser()
ap.add_argument("-dt","--dataset_train",type=str, required=True,help="(required) the train data directory")
ap.add_argument("-dv","--dataset_val",type=str, required=True,help="(required) the validation data directory")
ap.add_argument("-l","--labels",type=str, required=True,help="(required) the labelbinerizer")
args = vars(ap.parse_args())

lb = pickle.loads(open(args["labels"], "rb").read())
num_classes = len(lb.classes_)
logging.info("Number of classes: " + str(num_classes))
for cl in lb.classes_:
        logging.info("Classes: " + cl)

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
        args["dataset_train"],
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        args["dataset_val"],
        target_size=(image_size,image_size),
        batch_size=batch_size,
        class_mode='categorical')

pretrained_model = vgg16.VGG16(weights='imagenet', include_top=False, input_shape=(image_size, image_size, 3))

# Freeze all the layers
for layer in pretrained_model.layers[:-4]:
    layer.trainable = False

# Check the trainable status of the individual layers
#for layer in pretrained_model.layers:
#    print(layer, layer.trainable)
#    logging.info(str(layer), str(layer.trainable))

# Create the model
model = models.Sequential()

# Add the vgg convolutional base model
model.add(pretrained_model)

# Add new layers
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='softmax'))

""" model.add(layers.Flatten())
model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='softmax'))
 """
model.summary()

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])

# Checkpoints
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
checkpoint = ModelCheckpoint(model_name + ".h5", monitor='val_loss', verbose=1,save_best_only=True,save_weights_only=False, mode='min',period=1)
earlystop = EarlyStopping(monitor='val_acc', patience=15, verbose=0, mode='auto')
callbacks_list = [checkpoint, tensorboard, earlystop]

# Train the Model
# NOTE that we have multiplied the steps_per_epoch by 2. This is because we are using data augmentation.
history = model.fit_generator(
      train_generator,
      steps_per_epoch=2*train_generator.samples/train_generator.batch_size,
      epochs=epoch_amount,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples/validation_generator.batch_size,
      verbose=1,
      callbacks=callbacks_list)

# Save the Model
model.save(model_name + '.h5')

plotter = Plotter.TrainPlotter(history, epoch_amount, plot_file_name)
plotter.PlotLossAndAcc()

run_duration = (time() - start_time) / 60
end_msg = "Done! Run Duration:  " + str(run_duration) + " minutes."
print(end_msg)
logging.info(end_msg)
