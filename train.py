from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.callbacks import TensorBoard,ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.models import Model
from keras import optimizers 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from time import gmtime, strftime
from imutils import paths
from PIL import Image
from cnn import VGG16
from time import time
from helpers import Plotter 
import numpy as np
import argparse
import pathlib
import logging
import pickle
import os

# Manual Settings
file_postfix = "sbb1"

model_filepath = "model-" + file_postfix + ".h5"
lb_pickle_name = "lb-" + file_postfix + ".pickle"
tmp_data_dir = "tmp_data_" + file_postfix
tmp_val_dir = "tmp_val_" + file_postfix
epoch_amount = 50

# Use this: python train.py -d data
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
log_name = 'LOG_' + current_time + '.log'
logging.basicConfig(filename=log_name,level=logging.DEBUG)

##### Step-1:
############ Specify path to training and testing data. Minimum 100 images per class recommended.
############ Default image size is 160    
img_size=224
ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",type=str, required=True,help="(required) the train data directory")
#ap.add_argument("-train","--train_dir",type=str, required=True,help="(required) the train data directory")
#ap.add_argument("-val","--val_dir",type=str, required=True,help="(required) the validation data directory")
#ap.add_argument("-num_class","--class",type=int, default=2,help="(required) number of classes to be trained")
args = vars(ap.parse_args())

##### Step-2:
############ Do some random image transformations to increase the number of training samples
############ Note that we are scaling the image to make all the values between 0 and 1. That's how our pretrained weights have been done too
############ Default batch size is 8 but you can reduce/increase it depending on how powerful your machine is. 

# initialize the data and labels
data, labels, data_test, labels_test, tmp_data, tmp_labels = ([] for i in range(6))

# grab the image paths and prepare them for splitting
print("[INFO] loading images...")
logging.info("[INFO] loading images...")
image_paths = sorted(list(paths.list_images(args["dataset"])))

file_count = sum(len(files) for _, _, files in os.walk(args["dataset"]))
logging.info("Total number of files: " + str(file_count))

counter = 0
numFiles = 100
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
    out_path = tmp_data_dir + "/" + labels[idx]
    pathlib.Path(out_path).mkdir(parents=True, exist_ok=True) 
    img.save(out_path + "/" + name)

# Create temporary validation folder
counter = 0
print("[INFO]: Creating tmp validation data...")
for idx, img in enumerate(data_test):
    counter += 1
    name = (labels_test[idx] + str(counter) + ".jpg")
    out_path = tmp_val_dir + "/" + labels_test[idx]
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
        tmp_data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        tmp_val_dir,
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
#sys.exit()

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
callbacks_list = [checkpoint,tensorboard]


model = Model(inputs=base_model.input, outputs=predictions)

#model.compile(loss="categorical_crossentropy", optimizer=optimizers.SGD(lr=0.001, momentum=0.9),metrics=["accuracy"])
model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adam(),metrics=["accuracy"])
#model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adagrad(lr=0.01, epsilon=1e-08, decay=0.0),metrics=["accuracy"])

num_training_img=len(data)
num_validation_img=len(data_test)
stepsPerEpoch = num_training_img/batch_size
validationSteps= num_validation_img/batch_size
history = model.fit_generator(
        train_generator,
        steps_per_epoch=stepsPerEpoch,
        epochs=epoch_amount,
        callbacks = callbacks_list,
        validation_data = validation_generator,
        validation_steps=validationSteps
        )

plotter = Plotter.TrainPlotter(history, epoch_amount, file_postfix)
plotter.PlotLossAndAcc()

run_duration = time() - start_time
print("Processing time: ", run_duration)

logging.info("Done training! Duration: " + str(run_duration))



