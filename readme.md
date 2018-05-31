# CNN model for filtering out unwanted Stabi images
Created specifically to group Stabi images together that have meaningful content. This way less data is needed to be saved in the databank and clustering may be performed only on images with actual content.

---
## Dependencies:
Dependencies used for this are listed in the **requirements.txt** file. Download them easily to your current Python environment by navigating to the project root and entering the following:
* `pip install -r requirements.txt`

---
## Preparing data:
The script has been configured to locate the images by path, here being the **data** directory. Simply place all subdirectories within this directory. The subdirectories should then contain the images to be filtered. An example directory structure is as follows:

* data
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

The current version should run with the following command if images are properly placed in the **'data'** directory as suggested above:

`python classify-all.py --model filter_v2.model --labelbin label_v2.pickle --images data`

Once the script is done, an **'output'** directory will be created with subdirectories according to the number of classes the model was trained with.

Current subdirectories are:
* **blanks** (blank pages)
* **color_palette** (an image of a color palette)
* **content** (the images the we want)
* **logo** (the Stabi logo)
* **red_stamp** (red Stabi stamp mark)

### Note:
A single image may also be classifed for debugging purposes by running the **'classify-single'** script. Arguments for this are as follows:

`python classify-single.py --model filter_v2.model --labelbin label_v2.pickle --image data/0492_Page1_Block1.tif`

Make sure the last argument **'--image'** is pointing towards a single image file.


---
## Output:
Make sure there is no directory named **'output'** in the root location. An 'output' file will be created upon a successful run of the **'classify-all'** script. Images will be grouped by their predicted class followed by their directory name (usually the PPN name). The file names themselves remain the same as well as their file type, here TIFFs.

