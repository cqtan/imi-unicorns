 # This script calculates histograms based on the "Bag of Visual Words" model.
 # It is needed as a preprocessing step to calculate similar images.
 # 
 # Note: 
 #  All images are read from a local folder 'content'
 #  Extraction features from a pretained neural network with Keras is taken from:
 #  https://keras.io/applications/#resnet50


import os, shutil, random, pickle, sys, csv, traceback, warnings
import numpy as np
import matplotlib.pyplot as plt
import webcolors

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import DistanceMetric

from keras import applications
from keras.applications import resnet50

from keras import backend as K
from keras.models import Model

from keras.preprocessing.image import load_img, img_to_array

from skimage import io
from PIL import Image
from datetime import datetime
from scipy.spatial import distance



warnings.simplefilter('ignore', Image.DecompressionBombWarning)

images_new = []
images = []
bag = []
descriptors = []

feat_cluster_nums = [800]
dist = DistanceMetric.get_metric('euclidean')




def get_image(ppn_root):
    ppn_path = ppn_root + '/'
    image, pixels = read_image(ppn_path, file_name)
    if image is not None:
        new_name = dir_name + '_' + file_name
        images_new.append(new_name)
        return image, pixels
    else:
        return None, None
# end


def read_image(base_path, image):
    path = base_path + image
    try:
        original = Image.open(path).convert('RGB')
        # target size is determined by input size of neural network 
        resized = load_img(path, target_size=(224, 224))
        pixels = img_to_array(resized)
        return original, pixels
    except:
        print("Image ", path, ' cannot be opened!')
        return None, None
# end
    
def extract_features(pixels):
    # Extract features using a given pretrained model 

    image_batch = np.expand_dims(pixels, axis=0)
    processed_image = resnet50.preprocess_input(image_batch.copy())  
    intermediate_output = intermediate_layer_model.predict(processed_image)
    feature_vectors = np.reshape(intermediate_output, (-1, intermediate_output.shape[3]))

    return feature_vectors
# end

def reduce_feature_dimensions(features):
    # Normalize data with Standardscaler and reduce dimensions with PCA 
    
    features = scaler.transform(features)
    features = pca.transform(features)
    return features
# end


def generate_codebook(bag, feat_cluster_num):
    # Generate codebook with certain number of visual words based on given bag of words
    # KMeans Clustering will create centroids which represent the visual words
    # Returns:
    #   centroids = codebook

    start=datetime.now()
    print("Processing started at: ",start)
    # Use MiniBatchKMeans to speed up computation
    kmeans_feat = MiniBatchKMeans(feat_cluster_num, init_size=feat_cluster_num*3)
    kmeans_feat.fit(bag)
    end=datetime.now()-start
    print("Processing ended after: ",end)
    centroids = kmeans_feat.cluster_centers_

    with open('results.txt', 'a') as file: 
        file.write('Cluster-number: ' + str(feat_cluster_num) + '\n')
        file.write("Processing started at: "+ str(start) + '\n')
        file.write("Processing ended after: " +str(end) + '\n')
        file.write('Error: ' + str(kmeans_feat.inertia_) + '\n')
    return centroids
# end

def calculate_histogram(feature_vectors, codebook):
    # Calculate histogram of visual word frequencies for each given image
    # Note:
    #   Returned histograms are normalized ( = probabilities)


    histogram = np.zeros(codebook.shape[0])
    distances = dist.pairwise(feature_vectors, codebook)
    minimum_distance = np.argmin(distances, axis=1)
    
    min_dist_count = np.bincount(minimum_distance)

    histogram[minimum_distance] = min_dist_count[minimum_distance]
    histogram_norm = np.divide(histogram, np.sum(histogram))
    return histogram_norm
#end




# use the ResNet50 model to extract features
# 'layer_name' indicates which layer the features will be extracted from
# currently used layer is last convolutional layer -> featurevector size is 2048
model = applications.ResNet50(weights='imagenet', include_top=False)
layer_name = 'res5c_branch2c'
intermediate_layer_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)




## retrieve images from files

dir_start = 0 
file_start = 0

# in case of unexpected interruption use the saved pickle file to restart process
if os.path.exists("last_entry.txt"):
    with open("last_entry.txt",'r') as f:
        line = f.readline()
        split = line.split(',')
        if line:
            dir_start = int(split[0])
            file_start = int(split[1])
            if dir_start != 0 or file_start != 0:
                print('Importing files')
                images_new = pickle.load(open('images_new_names.pkl', 'rb'))
                bag = pickle.load(open('bag.pkl', 'rb'))
                descriptors = pickle.load(open('descriptors.pkl', 'rb'))
    print("indices for restart: " , dir_start , file_start)

# keep processing at starting index
is_at_index = False
try:
    for i, dir_name in enumerate(next(os.walk('./content'))[1]):
        print('directory index: ', i)       
        if 'PPN' in dir_name:
            ppn_root = os.path.join('./content/', dir_name)
            for j, file_name in enumerate(next(os.walk(ppn_root))[2]):
                if not is_at_index:
                    if i != dir_start or j != file_start:
                        pass
                    else:
                        is_at_index = True 
                        print('starting reading images at index: ', i, ' ', j)
                        im, pixels = get_image(ppn_root)
                        if im is not None:
                            feature_vectors = extract_features(pixels)
                            descriptors.append(feature_vectors)
            
                            for vector in feature_vectors: 
                                bag.append(vector)
            
                else:
                    im, pixels = get_image(ppn_root)

                    if im is not None:
                        feature_vectors = extract_features(pixels)
                        descriptors.append(feature_vectors)
            
                        for vector in feature_vectors: 
                            bag.append(vector)
        else:
            print('Not relevant: ', dir_name)

    K.clear_session()

except : 
    with open("err_log.txt",'w') as f:
        f.write('Error occurred at index: '+str(i)+','+str(j)+' - image: '+dir_name+','+file_name+'\n')
        f.write(traceback.format_exc())
    print('An error has occurred during file iteraion. Setting pickle files to last update.')
    
    raise SystemExit
    
finally:
    with open("images_new_names.pkl",'wb') as f:
        pickle.dump(images_new,f)

    with open("bag.pkl",'wb') as f:
        pickle.dump(bag,f)

    with open("descriptors.pkl",'wb') as f:
        pickle.dump(descriptors,f)

    with open("last_entry.txt",'w') as f:
        f.write(str(i)+','+str(j))

with open("last_entry.txt",'w') as f:
    f.write(str(i+1)+','+str(j+1))




## prepare data for BOVW
#  
#  Usage of StandardScaler and PCA is taken from:
#  https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60

bag = np.array(bag)
print("Current bag size: ", bag.shape)
scaler = StandardScaler()
bag_scaled =scaler.fit_transform(bag)
pca = PCA(.97)
feature_bag = pca.fit_transform(bag_scaled)
print("bag size after reducing dimensions: ", feature_bag.shape)
with open('results.txt', 'w') as file: 
    file.write(str(images_new) + '\n')




# create the histograms

cluster_num_index = 0

if os.path.exists("cluster_index.txt"):
    with open("cluster_index.txt",'r') as f:
        cluster_num_index = int(f.readline())

try:
    for index, feat_cluster_num in enumerate(feat_cluster_nums, cluster_num_index):
        print('index, cluster_num: ', index, feat_cluster_num)

        codebook = generate_codebook(feature_bag, feat_cluster_num)

        histogram_file_start = 0
        histograms = []

        histo_file_name = 'histograms_'+str(feat_cluster_num)+'.pkl'

        feature_vectors_all = []

        if os.path.exists("last_entry_histogram.txt"):
            with open("last_entry_histogram.txt",'r') as f:
                histogram_file_start = int(f.readline())
                if histogram_file_start != 0:
                    print('Importing histogram file')
                    histograms = pickle.load(open(histo_file_name, 'rb'))     
            print("index for histogram re-calculation: " , histogram_file_start)

        is_at_index = False       
        try:
            i = 0
            while i < len(images_new):
                if not is_at_index:
                    if i != histogram_file_start:
                        pass
                    else:
                        print('set to index at:', i)
                        is_at_index = True  
                        i -= 1
                else:
                    img_descs = np.array(descriptors[i])
                    feature_vectors = reduce_feature_dimensions(img_descs)

                    feature_vectors_all.append(feature_vectors)

                    histogram = calculate_histogram(feature_vectors, codebook)

                    histograms.append(histogram)
                i += 1
        except: 
            with open("err_log.txt",'a') as f:
                f.write('Error occurred at index: '+str(i)+'- image: '+images_new[i]+'\n')
                f.write(traceback.format_exc())
            print('An error has occurred during histogram calculation.')
            
            raise SystemExit

        finally:
            with open(histo_file_name,'wb') as f:
                pickle.dump(histograms,f)

            if not os.path.exists("cluster_index.txt"):
                with open("feature_vectors.pkl",'wb') as f:
                    pickle.dump(feature_vectors_all,f)

            with open("last_entry_histogram.txt",'w') as f:
                f.write(str(i))

        os.remove("last_entry_histogram.txt")

except:
    with open("err_log.txt",'a') as f:
        f.write('Error occurred at index: '+str(i)+'- image: '+images_new[i]+'\n')
        f.write(traceback.format_exc())
    print('An error has occurred during histogram calculationwith different cluster numbers.')
    
    raise SystemExit

finally:
    with open("cluster_index.txt",'w') as f:
        f.write(str(index))


with open("cluster_index.txt",'w') as f:
    f.write('0')

print('DONE PROCESSING!')

