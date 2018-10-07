# Pretrained VGGnet

Uses the pretrained VGGnet to classify certain classes and either outputs a json file specifically made for our SBB databank or outputs the images themselves in a categorized fashion. The goal is to be able to categorize the SBB images under certain categories and to create a file, which maps information of the images to their classified category.

Example JSON files can be viewed in the "JSONs" directory.

----
## Prepare training and validation data
Once you have training data (see first link below for tips in gathering them) the actual workflow can begin.

Splitting image data evenly is made easy with the use of the "datasplitter.py" script. Simply pass the path of the parent directory of all the images and it will create two separate directories, one for training and the other for validation (currently a ratio of 80% / 20% ). The directory structure is important though. 

The directories should also be named after their class. All of these directories should then be located within a parent directory, such as **'data'**. A possible directory structure is as follows:

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

Simply run the script with the directory, which has all the images, e.g., 

`python datasplitter.py -d data`

Output will be: 
* a directories for training, 
* a directory for validation 
* as well as the labels in form of a **.pickle** file, a.k.a. the Label-Binarizer.

---
## Train
Training can be done in two different ways.
* With "train.py" for using the VGGnet provided in the "cnn" directory.
    * `python train.py -t train-data/train -v train-data/val -l labels.pickle`
* With "imagenet_transfer.py" for using the VGGnet provided by Keras.
    * `python train_keras.py -t train-data/train -v train-data/val -l labels.pickle`

The first one was simply used as a starting point and to have a peek in to how the VGGnet is implemented. Using the second one with Keras simplifies it a bit more but in essence, they are very similar. Both perform preprocessing and augmentation of the data.

Output files are:
* model.h5 (the trained model file)
* A log file (logs time and classes)

---
## Predict

Once the model and label-binarizer have been created, then predictions can be made with though 2 version can be used again:
* "predict.py": Uses the weights you have trained (either with "train.py" or "train_keras.py")
    * `python predict.py -m model.h5 -l labels.pickle -d data`
* "predict_imagenet.py": Uses the weights available in Keras, specifically for Imagenet only. (This includes the top layer)
    * `python predict_imagenet.py -m model.h5 -l labels.pickle -d data`

(model and label-binarizer names may vary!)

Output files are:
* categories.json
* categories_alt.json
* another log file (logs time and classes)

Difference between the two is that the categories_alt.json includes the **accuracy** and **count** of the predicted labels. Reason for this, is to be able to sort images by their predicted accuracy, making images with high accuracy be shown first.
* Accuracies are Integers ranging from 75-100
* This, however, was never used but could potentially be useful for future projects!

---
## JSON file version 3 structure:

These are currently the JSON files with postfix '_alt'. They additionally add to the class occurrance also the predicted class' accuracy as well as the amount of occurrence (count). Please refer to the example JSON files in the "JSONs" directory.

The file itself has 3 sections:
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
        class-name2: count, 
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
## Notes
An 'ImageWriter' helper script has also been created to visualize output of images. With this, predicted images are written to a subfolder within the parent folder 'out' according to their predicted class.

Simply set the value of `write_images` to `True` in the "predict.py" script.

---
## References and Resources

A very useful script to get your hands on a lot of training data. This downloads images from Google Images in a very convenient way (JSON) with a lot of options.
* [https://github.com/hardikvasa/google-images-download](https://github.com/hardikvasa/google-images-download)

A short overview and introduction to Machine Learning and Convolutional Networks. Also includes iOS integration but that part can be left alone if not needed.
  * [https://www.raywenderlich.com/181760/beginning-machine-learning-keras-core-ml](https://www.raywenderlich.com/181760/beginning-machine-learning-keras-core-ml)

A Tutorial about training a model for your own needs. This includes data augmentation and Fine-Tuning a VGGnet.
* [https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)

A list of the models that are included in Keras and how to use them.
* [https://keras.io/applications/](https://keras.io/applications/)

Another Keras Fine-Tuning tutorial this time with food.
* [https://www.learnopencv.com/keras-tutorial-transfer-learning-using-pre-trained-models/](https://www.learnopencv.com/keras-tutorial-transfer-learning-using-pre-trained-models/)

Since object detection is also a possibility, here is a nice overview.
* [http://cv-tricks.com/object-detection/faster-r-cnn-yolo-ssd/](http://cv-tricks.com/object-detection/faster-r-cnn-yolo-ssd/)

For some tricks to improve the performance of your model when needed.
* [https://machinelearningmastery.com/improve-deep-learning-performance/](https://machinelearningmastery.com/improve-deep-learning-performance/)

An overview of evaluation metrics to be included every model.
* [https://machinelearningmastery.com/metrics-evaluate-machine-learning-algorithms-python/](https://machinelearningmastery.com/metrics-evaluate-machine-learning-algorithms-python/)

Alternative to ImageNet models: YOLO (an object detection model trained on the COCO dataset)
* [https://pjreddie.com/darknet/yolo/](https://pjreddie.com/darknet/yolo/)

Public Neural Network Models. Maybe you might find a good model as a basis.
* [https://www.gradientzoo.com/](https://www.gradientzoo.com/)






