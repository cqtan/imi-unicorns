# Pretrained VGGnet

Uses the pretrained VGGnet to classify certain classes and either outputs a json file specifically made for our SBB databank.

----
## Train
Training is now simplified to the point that only training data is needed that are grouped together in a folder. The folders should also be named after their class. All of these folders should then be located within a parent folder, such as 'data'. A possible folder structure is as follows:

data
* botany
    * 01.jpg
    * 02.jpg
    * 03.jpg
* crest
    * 01.jpg
    * ...
* handwriting
    * ...
* ...

Once training data has been placed within the root directory, the train.py script can be run with:

`python train.py -d data`

Output files are:
* model.h5 (the trained model file)
* lb.pickle (the label-binarizer, which houses all the labels)
* A log file

---
## Predict

Once the model and label-binarizer have been created, then predictions can be made with:

`python predict.py -m model-sbb1.h5 -l lb-sbb1.pickle -d data`

(model and label-binarizer names may vary!)

Output files are (currently):
* categories-18.json
* categories_alt-18.json
* another log file

(note: the '18' is amount of classes)

Difference between the two is that the categories_alt.json includes the **accuracy** and **count** of the predicted label. Reason for this, is to be able to sort images by their predicted accuracy, making images with high accuracy be shown first.
* Accuracies are Integers ranging from 75-100

---
### Note
An 'ImageWriter' helper script has also been created to visualize output of images. With this, predicted images are written to a subfolder within the parent folder 'out' according to their predicted class.

Simple include the commented lines with `ImageWriter...` in the predict.py script.

