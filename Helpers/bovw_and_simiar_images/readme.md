# Calculate similar images

Scripts to find the five most similar images for each image that is stored in the database. 

## Generating features

The script `features_resnet.py` is responsible for generating features which will be used as a basis to calculate similar images later on. 

### Feature extraction
It  extracts features from all images in the `content`-folder by use of a pretrained neural Network (ResNet50). 
The feature vectors are obtained from the last convolutional layer of the network (high level features). Each of these vectors has 2048 dimensions.

### Bag of visual words
All feature vectors are randomly stored together in a 'bag'.
The bag's resulting dimensionality (number of feature vectors * 2048) is reduced by applying a PCA afterwards to speed up computation time.
In the next step a clustering algorithm generates a 'codebook' with a defined number of 'visual words' (representative feature vectors). 
Eventually the script creates a histogram of visual words for each image. .  

## Nearest neighbors

Lastly, the script `ball_tree.py` recevies all histograms (currently of length 8500) and partitions this high-dimensional space using a ball tree. 
Similar images supposedly exhibit similar histograms, so the euclidean distance between them should be smaller than to differing images.
For every image the script queries the ball tree to obtain the five nearest neighbors.

The returned information is stored in a two-dimensional array. 
Each index (representing an image) contains an array with five entries which in turn contain the PPN and filename of the respective similar image.

The  array is saved as the HDF5-file `similarities.hdf5`

---

## Running the script

It is advisable to create a new virtual environment and install all dependencies from `requirements.txt`:

`pip install -r requirements.txt`

The script `features_resnet.py` needs to be extecuted at first. Acitvate the virtual environment, navigate to the folder where the script is located and run: 

`python features_resnet.py`

Once the first script has terminated, the second script can be run in the same manner:

`python ball_tree.py`

In case of unexpected interruption, rerun the script. 
All necessary information will be stored in external files which will then be used as a new starting point.  

---

## Note
 
As the script `features_resnet.py` uses the images from the `content`-folder both either need to be stored in the same location or the path 
that points to the folder has to be updated respectively. 

To run the script `ball_tree.py` the following files must be in located in the same folder:
* `images_new_names.pkl` -> created from `features_resnet.py`
* `histograms_XX.pkl` -> created from `features_resnet.py` (currently used `histograms_8500.pkl`)
* `image_ids.pkl` -> Not all images from the `content`-folder are stored in the database as well. 
This file contains all indices of images which actually are in the database to pick out 
the respective entries from `images_new_names.pkl` and `histograms_XX.pkl`
---

## References and helpful links

Detailed explanation of the concept 'Bag of Visual Words':
* https://gurus.pyimagesearch.com/the-bag-of-visual-words-model/ 

ResNet50:
* https://keras.io/applications/#resnet50 

Explanation of principal component analysis (PCA) and why it should be used:
* https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60

Ball Tree and how to use it with Scikit-Learn:
*https://en.wikipedia.org/wiki/Ball_tree
*http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html

