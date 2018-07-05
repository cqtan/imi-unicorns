from imutils import paths
import os

def CreateScaffold(outpath, labels):
    # Create output directory and subdirectories
    if not os.path.exists(outpath):
        os.mkdir(outpath)
        for cl in labels:
            os.makedirs(outpath + '/' + cl)


def WriteImage(outpath, label):
    
    pass
