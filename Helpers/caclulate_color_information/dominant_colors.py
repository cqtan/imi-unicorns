# Copyright 2018 David Zellhoefer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-


import os, random, pickle, sys, traceback, warnings
import numpy as np
import webcolors

from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import DistanceMetric

from PIL import Image
from datetime import datetime
from scipy.spatial import distance

warnings.simplefilter('ignore', Image.DecompressionBombWarning)

# number of clusters for the k-means algorithm
numberOfClusters=10 # (7 seems to be a good compromise)
w=h=256
size=w,h
color_infos = []

dir_start = 0 
file_start = 0


## retrieve images from file

def get_image(ppn_root):
    ppn_path = ppn_root + '/'
    image = read_image(ppn_path, file_name)
    if image is not None:
        image.thumbnail(size)

    return image
# end


def read_image(base_path, image):
    path = base_path + image
    try:
        original = Image.open(path).convert('RGB')
        return original
    except:
        return None
# end
    

## methods for calculating color information
# based on https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
# the following two methods are taken from the answer by "fraxel"
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]
# end

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name
# end of fraxel's code

def calculate_mean_color(pix):
    mean_color = np.mean(pix, axis=0)
    _, mean_color_name = get_colour_name(mean_color)
    mean_color_hex = webcolors.name_to_hex(mean_color_name)
    return mean_color_hex
# end


# taken from https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist
# end


def compute_distances(hist, rbg_from_names, dominant_colors_to_save):
    descending_color_freqs = np.copy(rbg_from_names, dominant_colors_to_save)
    max_val_index = np.argmax(hist)

    # delete color that has highest frquency -> will be in dominant colors anyway
    # use color as reference to compute distances to other colors
    descending_color_freqs = np.delete(descending_color_freqs, max_val_index, 0)
    max_val_color = np.reshape(rbg_from_names[max_val_index], (1,3))
    dominant_colors_to_save.append(max_val_color)

    descending_color_freqs = np.unique(descending_color_freqs, axis=0)
    dist_metric = DistanceMetric.get_metric('euclidean')
    distances = dist_metric.pairwise(max_val_color, descending_color_freqs)

    # sort distances from large to small -> chosen colors should be as distinct as possible
    return np.argsort(-distances), descending_color_freqs
#end


def fill_up_colors(dominant_colors_to_save, unique_colors, unique_counts, dominant_color_number):
    dominant_colors_to_save = unique_colors.tolist()
    counts_sorted = np.argsort(-unique_counts)

    # we need to fill up the number of colors -> use frequent colors multiple times
    # calculate how many colors are needed to complete dominant_color_number
    difference = dominant_color_number - len(unique_colors)
    missing_color_indices = np.arange(difference)
    colors_sorted = unique_colors[counts_sorted]
    if colors_sorted.shape[0] < difference:
        colors_to_add = np.tile(colors_sorted[0],(difference,1))
    else:
        colors_to_add = np.take(colors_sorted, missing_color_indices, axis=0)

    return np.concatenate((dominant_colors_to_save, colors_to_add), axis=0)
# end


def choose_colors(hist, rbg_from_names, dominant_colors_to_save, dominant_color_number):
    sorted_distance_indices, descending_color_freqs = compute_distances(hist, rbg_from_names, dominant_colors_to_save)
        
    dominant_colors_to_save = np.array(dominant_colors_to_save)
    dominant_colors_to_save = np.reshape(dominant_colors_to_save, (1,3))
    # only take the dominant_color_number-1 (since we have already added the most frequent color) 
    # most distinct colors to obtain a higher variance   
    dominant_color_indices = sorted_distance_indices[0,:dominant_color_number-1]
    chosen_dominant_colors = np.take(descending_color_freqs, dominant_color_indices, axis=0)

    return np.concatenate((dominant_colors_to_save, chosen_dominant_colors), axis=0)
# end



def calculate_color_information(im, dir_name, file_name):
    # open an image an convert it to RGB because we don't want to cope with RGB/RGBA conversions later on
    
    # scale the image down to speed up later processing (alas, this assumption has not been validated yet...)

    #print("Processing ended after: ",end)

    # 4 in case of RGBA
    #pix = np.array(im.getdata(),np.uint8).reshape(im.size[1], im.size[0], 3)

    # created a numpy array from the input image
    arr=np.array(im)
    # reshape the image for the clustering algorithm
    pix=arr.reshape((arr.shape[0] * arr.shape[1], 3))

    mean_color_hex =  calculate_mean_color(pix)


    # find the clusters as specified above
    clt = MiniBatchKMeans(n_clusters = numberOfClusters, random_state=0)
    clt.fit(pix)
    hist = centroid_histogram(clt)


    # the centroids will be floats but as RGB only allows integers we will round the whole array of centroids
    # print the verbal CSS name of each centroid
    rbg_from_names = []
    hex_codes = []
    dominant_colors_to_save = []
    dominant_color_number = 5

    for centroid in np.round(clt.cluster_centers_,0):
        _, closest_name = get_colour_name(centroid)
        name_2_rgb = webcolors.name_to_rgb(closest_name)
        rgb_entry = np.array([name_2_rgb[0], name_2_rgb[1], name_2_rgb[2]])
        rbg_from_names.append(rgb_entry)
        #print("\nActual colour name:", actual_name, ", closest colour name:", closest_name)

    rbg_from_names = np.array(rbg_from_names)
    unique_colors, unique_counts = np.unique(rbg_from_names, axis=0, return_counts=True)

    print('\nCalculating color info for', dir_name+'_'+file_name)

    # if unique colors == number of dominant colors we would like to extract -> just use this array
    if len(unique_colors) == dominant_color_number:
        dominant_colors_to_save = unique_colors

    elif len(unique_colors) < dominant_color_number:
        dominant_colors_to_save = fill_up_colors(dominant_colors_to_save, unique_colors, unique_counts, dominant_color_number)

    else:
        dominant_colors_to_save = choose_colors(hist, rbg_from_names, dominant_colors_to_save, dominant_color_number)


    for color in dominant_colors_to_save:      
        _, closest_name = get_colour_name(color)
        hex_codes.append(webcolors.name_to_hex(closest_name))

    hex_codes = np.array(hex_codes)

    return dominant_colors_to_save, hex_codes, mean_color_hex
# end



# in case of unexpected interruption use the saved pickle file to restart the process
# get starting index from last_entry txt-file
if os.path.exists("last_entry_color.txt"):
    with open("last_entry_color.txt",'r') as f:
        line = f.readline()
        split = line.split(',')
        if line:
            dir_start = int(split[0])
            file_start = int(split[1])
            if dir_start != 0 or file_start != 0:
                print('Importing files')
                color_infos = pickle.load(open('color_infos.pkl', 'rb'))
    print("indices for restart: " , dir_start , file_start)


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
                        im = get_image(ppn_root)
                        dominant_colors_to_save, hex_codes, mean_color_hex = calculate_color_information(im, dir_name, file_name)
                        dominant_colors_to_save = np.array(dominant_colors_to_save, float).flatten()
                        
                        info = (dir_name, file_name, dominant_colors_to_save.tolist(), hex_codes.tolist(), mean_color_hex)
                        color_infos.append(info)
            
                else:
                    im = get_image(ppn_root)
                    dominant_colors_to_save, hex_codes, mean_color_hex = calculate_color_information(im, dir_name, file_name)
                    dominant_colors_to_save = np.array(dominant_colors_to_save, float).flatten()

                    info = (dir_name, file_name, dominant_colors_to_save.tolist(), hex_codes.tolist(), mean_color_hex)
                    color_infos.append(info)
        else:
            print('Not relevant: ', dir_name)

except : 
    with open("err_log.txt",'w') as f:
        f.write('Error occurred at index: '+str(i)+','+str(j)+' - image: '+dir_name+','+file_name+'\n')
        f.write(traceback.format_exc())
    print('An error has occurred during file iteraion. Setting pickle files to last update.')
    
    raise SystemExit
    
finally:
    
    with open("color_infos.pkl",'wb') as f:
        pickle.dump(color_infos,f)

    with open("last_entry_color.txt",'w') as f:
        f.write(str(i)+','+str(j))

print('DONE')


