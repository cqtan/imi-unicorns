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
- bar_code
- blanks
- color_palette
- content
- logo
- red_stamp

Additionally, classifies images as 'other' if image is less than 85% classified as 'content'.
Also converts all images from TIFF to JPEG and saves them in the 'output' directory with 
their respective class and PPN.
'''

model_path1 = 'filter_v10.model'
labelbin_path1 = 'label_v10.pickle'
model_path2 = 'filter2_v3.model'
labelbin_path2 = 'label2_v3.pickle'
data_path1 = 'sbb/saved_images'
output_path1 = 'output1'
data_path2 = 'output1/content'
output_path2 = 'output2'

# Configure amount of GPU memory in % to allocate:
# config = tf.GPUOptions(per_process_gpu_memory_fraction=0.870)
# sess = tf.Session(config=tf.ConfigProto(gpu_options=config))

# Configure general logging
current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
log_name = 'LOG_' + current_time + '.log'
logging.basicConfig(filename=log_name,level=logging.DEBUG)

def filter_data(data_path, output_path, model, lb):
	# Log ppns as checkpoints
	logged_ppns = []
	counter = 0
	checkpoint_name = output_path + '_log' + '.txt' 
	if os.path.isfile(checkpoint_name):
		with open(checkpoint_name, 'r') as log_file:
			tmp = []
			tmp = log_file.readlines()
			for ppn in tmp:
				ppn = ppn[:-1] # Remove escape character
				logged_ppns.append(ppn)
			counter = len(logged_ppns)
			logging.info(str(datetime.now()) + ' ' + "Starting from checkpoint at: " + str(len(logged_ppns)))
	else:
		with open(checkpoint_name, 'w') as log_file:
			pass

	# loop over all images in each subdirectory
	print("[INFO] classifying images...")
	imagePaths = sorted(list(paths.list_images(data_path)))
	total_images = len(imagePaths)
	logging.info("Logging latest PPN classified...")
	last_ppn = ''
	for imagePath in imagePaths:
		ppn = imagePath.split(os.path.sep)[-2]

		if ppn not in logged_ppns:
			counter += 1
			print("Filtering image {:d} / {:d}".format(counter, total_images))
			# load and save a copy of the image
			image = Image.open(imagePath)
			output = image.copy()

			# Store image info
			filename = imagePath.split(os.path.sep)[-1]
			filename = filename[:-3]

			# pre-process the image for classification
			image = image.resize((96, 96))
			image = np.array(image)
			image = np.divide(image, 255.0)
			image = np.expand_dims(image, axis=0)

			# classify the input image
			proba = model.predict(image)[0]
			idx = np.argmax(proba)
			label = lb.classes_[idx]
			highest_pred = proba[np.argsort(proba)[-1:]]
			if label == 'content' and highest_pred < 0.85:
				label = 'outlier'
				print('[INFO] Check outlier directory: ', ppn + ', ' + filename)
				logging.info('Check outlier directory: ' + ppn + ', ' + filename)

			# within the predicted subdirectory of the class create
			# another subdirectory according to the PPN of the image.
			out_path = output_path+'/'+label+'/'+ppn
			if not os.path.exists(out_path):
				os.makedirs(out_path)
			output.save(os.path.join(out_path,filename)+'jpg')

			# Log latest PPN
			if last_ppn != ppn:
				last_ppn = ppn
				logging.info(str(datetime.now()) + ' ' + str(ppn))
				with open(checkpoint_name, 'a') as log_file:
					log_file.write(str(ppn) + '\n')

# load the trained convolutional neural network and the label binarizer, then filter
print("[INFO] loading 1st network...")
logging.info(str(datetime.now()) + ' ' + 'Loading 1st network.')

model1 = load_model(model_path1)
lb1 = pickle.loads(open(labelbin_path1, "rb").read())

# Create output directory and subdirectories
if not os.path.exists(output_path1):
	os.mkdir(output_path1)
	for cl in lb1.classes_:
		os.makedirs(output_path1 + '/' + cl)

filter_data(data_path1, output_path1, model1, lb1)

# load the trained convolutional neural network and the label binarizer, then filter
print("[INFO] loading 2nd network...")
logging.info(str(datetime.now()) + ' ' + 'Loading 2nd network.')

model2 = load_model(model_path2)
lb2 = pickle.loads(open(labelbin_path2, "rb").read())

# Create output directory and subdirectories
if not os.path.exists(output_path2):
	os.mkdir(output_path2)
	for cl in lb2.classes_:
		os.makedirs(output_path2 + '/' + cl)

filter_data(data_path2, output_path2, model2, lb2)

print("[INFO] Done!")
logging.info(str(datetime.now()) + "DONE!!!")

