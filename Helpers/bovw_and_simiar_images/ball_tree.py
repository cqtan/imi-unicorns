# This script calculates similar images based on histograms of visual words.
# Histograms are stored in a ball tree which is used to retrieve 5 images with least distance to each query image
#
# Note: 
#   The script needs the following data in order to run:
#   images_new_names.pkl -> created from features_resnet.py
#   histograms_XX.pkl -> created frm features_resnet.py
#   image_ids.pkl
# 
#   How to use the ball tree is explained in: 
#   http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html


import os, pickle, traceback, random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import BallTree
from datetime import datetime

import h5py



def extract_elements(data, indices):
    # Retrieve only relevant images and histograms.
    # Not all images that have been calculate histograms for are stored in database,
    # so select only images that can actually be found in database to make sure that results for similar images are in database

    new_data = np.take(data, indices, axis=0) 

    return new_data
# end


def create_ball_tree(query_hists):
    # Create ball tree from histograms.
    
    start_tree=datetime.now()   
    print("Processing tree started at: ",start_tree)
    tree = BallTree(query_hists, leaf_size=300)  
    end_tree=datetime.now()-start_tree
    print("Current processing time for creating tree: ",end_tree,'\n')
    return tree
# end



indices = np.array(pickle.load(open('image_ids.pkl', 'rb')))

histograms = np.array(pickle.load(open('histograms_8500.pkl', 'rb'))) 
images = np.array(pickle.load(open('images_new_names.pkl', 'rb')))

query_hists = extract_elements(histograms, indices)
query_imgs = extract_elements(images, indices)

with open("images_names_reduced.pkl",'wb') as f:
    pickle.dump(query_imgs,f)

# files are pretty big and as they are not needed anymore, memory should be deallocated
del histograms  
del images

tree = create_ball_tree(query_hists) 


# in case of unexpected interruption use the saved file to restart process
img_distances, img_indices = [], []
if os.path.exists('img_distances.hdf5'):
    print('importing precalculated indices and distances')

    img_indices = None
    with h5py.File('img_indices.hdf5', 'r') as f:
        img_indices = np.array(f.get('indices'))

    img_distances = None
    with h5py.File('img_distances.hdf5', 'r') as f:
        img_distances = f.get('distances')


# if files have not been created, query the tree and create files
else:
    img_distances, img_indices = tree.query(query_hists, k=3)     
    print(img_indices)

    with h5py.File('img_indices.hdf5', 'w') as f:
        f.create_dataset("indices", data=img_indices)
    with h5py.File('img_distances.hdf5', 'w') as f:
        f.create_dataset("distances", data=img_distances)



similarities = []
similarities_start = 0

if os.path.exists("last_entry_similarities.txt"):
    with open("last_entry_similarities.txt",'r') as f:
        similarities_start = int(f.readline())
        if similarities_start != 0:
            print('Importing similarity results')

            with h5py.File('similarities.hdf5', 'r') as f:
                similarities = np.array(f.get('similarities')).tolist()
           
    print("starting at index: " , similarities_start)


start=datetime.now()   
print("Processing started at: ",start)

# keep processing at starting index
is_at_index = False    
try:
    i = 0   
    while i < len(query_imgs):
        if not is_at_index:
            if i != similarities_start:
                print('passing')
                pass
            else:
                print('set to index at:', i,'\n')
                is_at_index = True  
                i -= 1
       
        else:
            if i % 100 == 0:
                print('calculating similar images for image ', query_imgs[i])
                end=datetime.now()-start
                print("Current processing time: ",end,'\n')

            query_img_info = []
            # you will get k indices for each query image 
            inds = img_indices[i]
            current_img = query_imgs[i]
            split = current_img.split('_', 1)
            query_img_ppn = split[0].split('PPN')
            query_img_name = split[1]

            sim_images = []
            for j, similar_img in enumerate(query_imgs[inds]):
                similar_img_info = []
                split = similar_img.split('_', 1)
                similar_img_ppn = split[0].split('PPN')
                similar_img_name = split[1]

                # if j == 0, similar image is query image itself -> just skip this one
                if j != 0:
                    similar_img_info.append(str.encode(similar_img_ppn[1]))
                    similar_img_info.append(str.encode(similar_img_name))
                    sim_images.append(similar_img_info)

            # similarities contains for each image an array with k-1 elements which in turn only contain the ppns and names of these images
            # in order to store results in database you will need the images_names_reduced.pkl as they are mapped through their indices
            similarities.append(sim_images)
            
        i += 1

except: 
    if os.path.exists("err_sim_log.txt"):
        with open("err_sim_log.txt",'a') as f:
            f.write('Error occurred at index: '+str(i)+'- image: '+current_img+'\n')
            f.write(traceback.format_exc())
    else:
        with open("err_sim_log.txt",'w') as f:
            f.write('Error occurred at index: '+str(i)+'-> image: '+current_img+'\n')
            f.write(traceback.format_exc())
    print("An error occurred at index ", i)
    raise SystemExit


finally:    
    similarities = np.array(similarities)
    with h5py.File('similarities.hdf5', 'w') as f:
        f.create_dataset("similarities", data=similarities)

    with open("last_entry_similarities.txt",'w') as f:
        f.write(str(i))


end = datetime.now()
diff=end-start
print("Processing ended at: ",end)
print("Processing ended after: ",diff)

