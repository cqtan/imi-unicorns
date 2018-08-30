from PIL import Image
import os

# Path of Image-folders
rootdir ='PATH/TO/IMAGES'
# The height, the images should have
thumb_height = 200
folders = [f.path for f in os.scandir(rootdir) if f.is_dir() ]

for entry in folders:
    print("Current directory: " + entry)
    subfolders = [s.path for s in os.scandir(entry) if s.is_dir() ] 
    for PPN in subfolders:
        #if os.path.isdir(directory):
        print_ppn = PPN.split("/")
        print_ppn = print_ppn[len(print_ppn)-1]
        print("Current PPN: " + print_ppn)
        ppn_directory = PPN
        for image_file in os.scandir(ppn_directory):
            if image_file.is_file():
                print("Current file: " + image_file.name)
                if "_thumb" not in image_file.name:
                    im_path = image_file.path
                    image = Image.open(im_path)
                    width, height = image.size
                    image.load()
                    size = (width * (thumb_height/ height), thumb_height)
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(im_path.replace('.jpg', '') + '_thumb.jpg', 'JPEG')
                