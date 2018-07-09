# Pretrained VGGnet

Uses the pretrained VGGnet to classify certain classes and either outputs a json file specifically made for our SBB databank.

If you simply need the production JSON file then use either of the JSON files that has **'_prod'** in their names. The one that also has **'_alt'** (version 3) includes more data other than the classes, i.e., accuracy and occurrences (count).

Currently latests: **categories-18.json** or **categories_alt-18.json**

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

## JSON file version 3 structure:

These are currently the JSON files with postfix '_alt'. They additionally add to the class occurrance also the predicted class' accuracy as well as the amount of occurrence (count).

The file itself is has 3 sections:
* category_data
* book_data
* image_data


```
category_data: {
    UI-name: {
        backend-name: count
    },
    ...
}, 
book_data: {
    ppn: {
        class-name1: count,
        class-name2: count}, 
        ...
    }, 
    ...
},
image_data: [
    {
        classes: {
            class-name1: accuracy,
            class-name2: accuracy,
            ...
        }, 
        path: actual-path, 
        ppn: actual-ppn
    }, 
    ...
]
```

---
### Note
An 'ImageWriter' helper script has also been created to visualize output of images. With this, predicted images are written to a subfolder within the parent folder 'out' according to their predicted class.

Simple include the commented lines with `ImageWriter...` in the predict.py script.

