from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils import paths
import numpy as np
#import tensorflow as tf
import argparse
import pickle
from PIL import Image
import os
import logging
from time import gmtime, strftime
from datetime import datetime

'''
Reads all images listed in the 'data_path' variable and classifies images according to
the classes in listed in the label.pickle file. Currently:
- blanks
- color_palette
- content
- logo
- red_stamp

Additionally, classifies images as 'other' if image is less than 85% classified as 'content'.
Also converts all images from TIFF to JPEG and saves them in the 'output' directory with 
their respective class and PPN.
'''

# Configure amount of GPU memory in % to allocate:
# config = tf.GPUOptions(per_process_gpu_memory_fraction=0.870)
# sess = tf.Session(config=tf.ConfigProto(gpu_options=config))

# Configure logging
current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
logging.basicConfig(filename='LOG_' + current_time + '.log',level=logging.DEBUG)

model_path = 'filter_v2.model'
labelbin_path = 'label_v2.pickle'
data_path = 'data'

# load the trained convolutional neural network and the label
# binarizer
print("[INFO] loading network...")
model = load_model(model_path)
lb = pickle.loads(open(labelbin_path, "rb").read())

# Create output directory and subdirectories
if not os.path.exists('output'):
	os.mkdir('output')
	for cl in lb.classes_:
		os.makedirs('output/'+cl)

# loop over all images in each subdirectory
print("[INFO] classifying images...")
imagePaths = sorted(list(paths.list_images(data_path)))
logging.info("Logging latest PPN classified...")
last_ppn = ''
for imagePath in imagePaths:
	# load and save a copy of the image
	image = Image.open(imagePath)
	output = image.copy()

	# Store image info
	filename = imagePath.split(os.path.sep)[-1]
	filename = filename[:-3]
	ppn = imagePath.split(os.path.sep)[-2]
	if last_ppn != ppn:
		last_ppn = ppn
		logging.info(str(datetime.now()) + ' ' + ppn)

	# pre-process the image for classification
	image = image.resize((96, 96))
	image = np.array(image)
	image = np.divide(image, 255.0)
	image = np.expand_dims(image, axis=0)

	# classify the input image
	proba = model.predict(image)[0]
	idx = np.argmax(proba)
	label = lb.classes_[idx]
	if label == 'content' and (proba[np.argsort(proba)[-1:]]) < 0.85:
		label = 'other'
		print('[INFO] Check unidentified content in others directory: ', ppn + ', ' + filename)
		logging.info('Check unidentified content in others directory: ' + ppn + ', ' + filename)

	# within the predicted subdirectory of the class create
	# another subdirectory according to the PPN of the image.
	out_path = 'output/'+label+'/'+ppn
	if not os.path.exists(out_path):
		os.makedirs(out_path)
	output.save(os.path.join(out_path,filename)+'jpg')

	# Log latest PPN
	if last_ppn != ppn:
		last_ppn = ppn
		logging.info(datetime.now() + ' ' + ppn)

print("[INFO] Done! Output directory created!")
