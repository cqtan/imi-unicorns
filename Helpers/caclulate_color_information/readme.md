# Calculate color information of SBB images

## Synopsis

The script `dominant_colors.py` is used to calculate dominant colors as well as mean colors of all images 
that are stored in the `content`-folder which had been created by the script `classify-all.py`. 

---

## Features

### Dominant colors

Dominant colors are the N most frequent colors that occur in an image and they can be used to describe the image. 
Matching dominant colors of images is an easy and fast way to possibly determine similar images as these are more likely to have similar colors. Dominant colors are found by clustering all colors of an image. 

The script `dominant_colors.py` applies the MiniBatchKMeans-Algorithm that is provided by the Scikit-Learn framework.

### Mean colors

Mean colors are less useful to identify similar images. However, providing that data allows to implement a functionality in the application that filters the results by a certain color.

## Running the script

It is advisable to create a new virtual environment and install all dependencies from `requirements.txt`:

`pip install -r requirements.txt`

Activate the virtual environment, navigate to the folder where the script is located and run: 

`python dominant_colors.py`

In case of unexpected interruption rerun the script. 
All information that had been calculated before will be stored in the `color_infos.pkl` file which in turn will be used as a starting point.  

---

## Note

Most of the images are rather monochromatic. To achieve a better representation of the images it is useful to obtain colors which are as different but still as frequent as possible. Therefore, the clustering was performed with a higher cluster number. The number of colors is reduced afterwards.

As the script uses the images from the `content`-folder both either need to be stored in the same location or the path 
that points to the folder has to be updated respectively. 

The resulting `.pkl` file contains the following information: 
* RGB-values of the dominant colors
* Hexadecimal codes of the dominant colors
* Hexadecimal codes of the mean colors
* PPN 
* Filename

---

## References

Detailed explanation of the K-Means Algorithm and how to use it with Scikit-Learn
* https://towardsdatascience.com/clustering-using-k-means-algorithm-81da00f156f6 
* http://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html#sklearn.cluster.MiniBatchKMeans
