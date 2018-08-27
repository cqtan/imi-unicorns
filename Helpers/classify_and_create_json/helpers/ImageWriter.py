from imutils import paths
import os

def CreateScaffold(outpath, labels):
    # Create output directory and subdirectories
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        for cl in labels:
            os.makedirs(outpath + '/' + cl)


def WriteImageWithPpn(image, outpath, image_path, label):
    output = image
    ppn = image_path.split(os.path.sep)[-2]
    filename = image_path.split(os.path.sep)[-1]
    filename = filename[:-3]

    out_path = outpath+'/'+label+'/'+ppn
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_path = os.path.join(out_path,filename) + 'jpg'
    print("Writing image to: " + out_path)
    output.save(out_path)

def WriteImage(image, outpath, image_path, label, confidence):
    output = image
    out_path = outpath+'/'+label
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_path = os.path.join(out_path,label) + "-" + str(confidence) + '.jpg'
    #print("Writing image to: " + out_path)
    output.save(out_path)