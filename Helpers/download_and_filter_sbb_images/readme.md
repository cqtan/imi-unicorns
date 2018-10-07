# CNN algorithms for filtering out unwanted Stabi images
Created specifically to group Stabi images together that have meaningful content. This way less data is needed to be saved in the databank and clustering may be performed only on images with actual content. Furthermore, the TIFF images are converted to JPEG. Instead of processing data amounting close to 1 terabyte, only around 80 GB are considered instead with the help of the following steps.

---
## Dependencies:
Dependencies used for this are listed in the **requirements.txt** file. Download them easily to your current Python environment (or switch to virtual one) by navigating to the project root and entering the following:
* `pip install -r requirements.txt`

Or when using Anaconda:
* First, add these to the conda channels to install packages outside from the default channels:
    * `conda config --append channels conda-forge`
    * `conda config --append channels gilbertfrancois`
* Then install the packages listed in the 'package-list.txt' with:
    * `conda install --file package-list.txt`

Note: This part of the project was primarily developed on a Windows 10 computer since the GPU (GTX 980ti) was used for it's higher computational speed. Support for specific versions of dependencies may, therefore, differ depending on the OS.

---
## Downloading the SBB images:

One of the first steps of this project was to download the SBB images. Run the following download SSB images:
* `python sbbget.py`

This should download the images to the **sbb/saved_images** directory. Since this is an enormous amount of data (ca.  Terabyte) be prepared to let the code run for a while. If the script is interrupted, simply rerun the interrupted script. It should pick up where it left off or when in doubt, check the last section about **Output and Logging**.

---
## Creating the model for filtering:

After downloading the SBB images, filtering out the images that were considered as unimportant was the second step. For this, certain images were **manually hand-picked** from the SBB images and grouped together according to their category. At the time of this project there was an imbalance in the number of images of certain categories in which case the filtering process would be biased. Furthermore, it was also assumed that certain categories were hard for the model to properly distinguish from other categories. Therefore, 2 separate datasets were created for training:

dataset1:

* **blanks** (Blank pages)
* **color_palette** (An image of a color palette)
* **content** (The images that we want) 

dataset2:
* **bar_code** (Stabi bar codes)
* **covers** (Simple book covers, complex ones are left out)
* **logo** (The Stabi logo)
* **red_stamp** (Red Stabi stamp mark)
* **content** (The images that we want)

With this, 2 different models with their associated class labels (pickle file created by the LabelBinarizer) were created by running the `train_filter.py` script twice.

* `python train_filter.py -d train_images1 -m filter1.model -l label1.pickle -p plot1.png`
* `python train_filter.py -d train_images2 -m filter2.model -l label2.pickle -p plot2.png`
* The following are short explanations to the individual parameters:
    * -d: path to input dataset for training (i.e., directory of images)
    * -m: path to output model
    * -l: path to output label binarizer
    * -p: path to output accuracy/loss plot.png

The model will then be used for the classification tasks in the next section while the pickle file provides the labels (category name / class) of the classified images. A plot.png file is also created for simple evaluation purposes. 

---
## Filter the SBB images:

This **classify-all.py** script has been configured to perform 2 filtering processes since 2 models were made during the training phase. The downloaded SBB images are required here and they should be in the **sbb** directory.  The subdirectories should then contain the images to be filtered. An example directory structure is as follows:

* sbb
    * saved_images
        * PPN61019657X
            * 0001_Page1_Block2.tif
            * 0001_Page1_Block12.tif
            * 0132_Page1_Block9.tif
            * ...
        * PPN610195530
            * ...
        * PPN610195867
            * ...
        * PPN610196898
            * ...
        * ...


The paths to the location of the images, models and pickle files were specified at the beginning of the script itself and should be modified depending if the name or location of these files are changed.
Simply run the following to perform the filtering of the SBB images:
* `python classify-all.py` 

Once the script is done, **'output'** directories will be created with subdirectories according to the number of classes the model was trained with. The images that we want and that are considered to have meaningful content are located in the directory specified in the `output_path2` variable in the **content** subdirectory.


### Note:
A single image may also be classifed for debugging purposes by running the **'classify-single'** script. Arguments for this are as follows:

`python classify-single.py --model filter_v2.model --labelbin label_v2.pickle --image data/0492_Page1_Block1.tif`

Make sure the last argument **'--image'** is pointing towards a single image file.



---
## Output and Logging:
The **output1** and **output2** directories will be created (if not already). Images will be grouped by their predicted class followed by their directory name (usually the PPN name). The file names themselves remain the same as well though they will instead be converted to JPEG imges to save space.

Log files will also be created to keep track of the progress of the download and classify scripts. Make sure to check them if errors occur or when scripts are interrupted.

The first script will continue where it left off if unterrupted and if the respective **ppn_log.txt** has been created on the first run.

The second script also continues where it left off if interrupted by reading both the **output1_log.txt** and **output2_log.txt**. These two will simply list the PPNs that it has already dealt with and check against the newly read. Simply rerun `python classify-all.py` if this happens.

The **LOG_2018_.log** simply lists more information on the filtering progress for each run of the `classify-all.py` script.

