# CNN model for filtering out unwanted Stabi images
Created specifically to group Stabi images together that have meaningful content. This way less data is needed to be saved in the databank and clustering may be performed only on images with actual content. Furthermore, the TIFF images are converted to JPEG.

---
## Dependencies:
Dependencies used for this are listed in the **requirements.txt** file. Download them easily to your current Python environment by navigating to the project root and entering the following:
* `pip install -r requirements.txt`

---
## tl;dr:
Run the following to first download SSB images:
* `python sbbget.py`

Once all images from the **OCR-PPN-Liste.txt** have been downloaded to **sbb/saved_images**, run:
* `python classify-all.py`

Output files **output1** and **output2** will be created but only the latter is of concern. Meaningful content should then be in **output2/content**. Double check other directories for outliers though!

---
## Preparing data:
The following sections explain in more detail the workflow of the scripts.

The script has been configured to locate the images by path, here being the **ssb** directory. Simply place all subdirectories within this directory. The subdirectories should then contain the images to be filtered. An example directory structure is as follows:

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

---
## Running the script:
The only script you have to run is the **'classify-all'** script. The arguments to be passed are as follows:

* model: path to trained model model.
* labelbin: path to label binarizer.
* images: path to input images.

The current version should run with the following command if images are properly placed in the **'sbb'** directory as suggested above:

`python classify-all.py`

Once the script is done, **'output'** directories will be created with subdirectories according to the number of classes the model was trained with.

Due to imbalance in training data, two models were trained to filter the images. The first model filters the following:
* **blanks** (Blank pages)
    * ca. 1500 training data.
* **color_palette** (An image of a color palette)
    *  ca. 200 training data.
* **content** (The images the we want) 
    * ca. 1700 training data.

The second model filters the following:
* **bar_code** (Stabi bar codes)
* **covers** (Simple book covers, complex ones are left out)
* **logo** (The Stabi logo)
* **red_stamp** (Red Stabi stamp mark)
* **content** (The images the we want)

### Note:
A single image may also be classifed for debugging purposes by running the **'classify-single'** script. Arguments for this are as follows:

`python classify-single.py --model filter_v2.model --labelbin label_v2.pickle --image data/0492_Page1_Block1.tif`

Make sure the last argument **'--image'** is pointing towards a single image file.

---
## Output and Logging:
The **output1** and **output2** directories will be created (if not already). Images will be grouped by their predicted class followed by their directory name (usually the PPN name). The file names themselves remain the same as well though they will instead be converted to JPEG iamges to save space.

Log files will also be created to keep track of the progress of both scripts. Make sure to check them if errors occur or when scripts are interrupted.

The first script will continue where it left off if unterrupted if the respective **ppn_log.txt** has been created.

The second script requires manual intervention when interrupted to pick off where it stopped since the order of PPN can be mixed. Hence, remove PPN directories listed in the last **LOG_2018_.log** file out of the **sbb/saved_images** directory and rerun the script `python classify-all.py`. 

