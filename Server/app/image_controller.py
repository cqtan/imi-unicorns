from app import db
from bson.json_util import dumps
from bson.objectid import ObjectId


class Image_Controller:

    def get_images_by_feature(self, feature):
        images = db.images.find({"features": feature})

        return dumps(images)

    def get_one_image_by_feature(self, feature):
        image = db.images.find_one({"features": feature})

        return dumps(image)

    def get_images_by_subject(self, subject):
        images = db.images.find({"subject": subject})

        return dumps(images)

    def get_one_image_by_subject(self, subject):
        image = db.images.find_one({"subject": subject})

        return dumps(image)

    def get_images_by_color(self, color):
        images = db.images.find({"colors": color})

        return dumps(images)

    def get_image(self, object_id):
        print('ObjectID: ', ObjectId(object_id))
        image = db.images.find({"_id": ObjectId(object_id)})

        return dumps(image)
